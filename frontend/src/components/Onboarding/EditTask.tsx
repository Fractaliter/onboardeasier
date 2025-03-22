import { useMutation, useQueryClient } from "@tanstack/react-query";
import { type SubmitHandler, useForm } from "react-hook-form";

import {
  Button,
  DialogActionTrigger,
  DialogRoot,
  DialogTrigger,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react";
import { useState } from "react";
import { FaExchangeAlt } from "react-icons/fa";

import { type TaskPublic, type TaskUpdate,TasksService }  from "@/client"
import type { ApiError } from "@/client/core/ApiError";
import useCustomToast from "@/hooks/useCustomToast";
import { handleError } from "@/utils";
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";
import { Field } from "../ui/field";

interface EditTaskProps {
  Task: TaskPublic;
}

const EditTask = ({ Task }: EditTaskProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const queryClient = useQueryClient();
  const { showSuccessToast } = useCustomToast();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<TaskUpdate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: Task,
  });

  const mutation = useMutation({
    mutationFn: (data: TaskUpdate) =>
      TasksService.updateTask(Task.id,{ taskId: Task.id, requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Task updated successfully.");
      reset();
      setIsOpen(false);
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
    onError: (err: ApiError) => {
      handleError(err);
    },
  });

  const onSubmit: SubmitHandler<TaskUpdate> = async (data) => {
    mutation.mutate(data);
  };

  return (
    <DialogRoot
      size={{ base: "xs", md: "md" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm">
          <FaExchangeAlt fontSize="16px" />
          Edit Task
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Task</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the Task details below.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.title}
                errorText={errors.title?.message}
                label="Task Name"
              >
                <Input
                  id="title"
                  {...register("title", {
                    required: "Task title is required",
                  })}
                  placeholder="Task title"
                  type="text"
                />
              </Field>

              <Field
                invalid={!!errors.status}
                errorText={errors.status?.message}
                label="Status"
              >
                <Input
                  id="status"
                  {...register("status")}
                  placeholder="Status"
                  type="text"
                />
              </Field>

              <Field
                invalid={!!errors.description}
                errorText={errors.description?.message}
                label="Description"
              >
                <Input
                  id="description"
                  {...register("description")}
                  placeholder="Description"
                  type="text"
                />
              </Field>

              <Field
                invalid={!!errors.assignedMemberId}
                errorText={errors.assignedMemberId?.message}
                label="AssignedMember"
              >
                <Input
                  id="assignedMemberId"
                  {...register("assignedMemberId")}
                  placeholder="AssignedMember"
                  type="text"
                />
              </Field>
            </VStack>
          </DialogBody>

          <DialogFooter gap={2}>
            <DialogActionTrigger asChild>
              <Button variant="subtle" colorPalette="gray" disabled={isSubmitting}>
                Cancel
              </Button>
            </DialogActionTrigger>
            <Button variant="solid" type="submit" loading={isSubmitting}>
              Save
            </Button>
          </DialogFooter>
          <DialogCloseTrigger />
        </form>
      </DialogContent>
    </DialogRoot>
  );
};

export default EditTask;
