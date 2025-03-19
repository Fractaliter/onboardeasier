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

import { type ProjectPublic, type ProjectUpdate,ProjectsService }  from "@/client"
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

interface EditProjectProps {
  project: ProjectPublic;
}

const EditProject = ({ project }: EditProjectProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const queryClient = useQueryClient();
  const { showSuccessToast } = useCustomToast();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProjectUpdate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: project,
  });

  const mutation = useMutation({
    mutationFn: (data: ProjectUpdate) =>
      ProjectsService.updateProject(project.id,{ projectId: project.id, requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Project updated successfully.");
      reset();
      setIsOpen(false);
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
    onError: (err: ApiError) => {
      handleError(err);
    },
  });

  const onSubmit: SubmitHandler<ProjectUpdate> = async (data) => {
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
          Edit Project
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Project</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the project details below.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.name}
                errorText={errors.name?.message}
                label="Project Name"
              >
                <Input
                  id="name"
                  {...register("name", {
                    required: "Project name is required",
                  })}
                  placeholder="Project Name"
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
                  placeholder="Project Description"
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

export default EditProject;
