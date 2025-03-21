import React from "react";
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm, Controller } from 'react-hook-form';
import {
  Button,
  DialogActionTrigger,
  DialogTitle,
  Input,
  Select,
  Text,
  VStack,
} from '@chakra-ui/react';
import { useState } from 'react';
import { FaPlus } from 'react-icons/fa';
import { TasksService, TaskCreate, TaskStatusEnum } from '@/client';
import { ApiError } from '@/client/core/ApiError';
import useCustomToast from '@/hooks/useCustomToast';
import { handleError } from '@/utils';
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTrigger,
} from '../ui/dialog';
import { Field } from '../ui/field';

const AddTask = () => {
  const [isOpen, setIsOpen] = useState(false);
  const queryClient = useQueryClient();
  const { showSuccessToast } = useCustomToast();
  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors, isValid, isSubmitting },
  } = useForm<TaskCreate>({
    mode: 'onBlur',
    criteriaMode: 'all',
    defaultValues: {
      title: '',
      description: '',
      projectId: '',
      assignedMemberId: '',
      status: TaskStatusEnum.PENDING // Ensure 'status' is included
    },
  });

  const mutation = useMutation({
    mutationFn: (data: TaskCreate) => TasksService.createTask(data),
    onSuccess: () => {
      showSuccessToast('Task created successfully.');
      reset();
      setIsOpen(false);
    },
    onError: (err: ApiError) => {
      handleError(err);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const onSubmit = (data: TaskCreate) => {
    mutation.mutate(data);
  };

  return (
    <DialogRoot
      size={{ base: 'xs', md: 'md' }}
      placement='center'
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger asChild>
        <Button value='add-task' my={4}>
          <FaPlus fontSize='16px' />
          Add Task
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Task</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Fill in the details to add a new task.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.title}
                errorText={errors.title?.message}
                label='Title'
              >
                <Input
                  id='title'
                  {...register('title', {
                    required: 'Title is required.',
                  })}
                  placeholder='Title'
                  type='text'
                />
              </Field>

              <Field
                invalid={!!errors.description}
                errorText={errors.description?.message}
                label='Description'
              >
                <Input
                  id='description'
                  {...register('description')}
                  placeholder='Description'
                  type='text'
                />
              </Field>

              <Field
                required
                invalid={!!errors.projectId}
                errorText={errors.projectId?.message}
                label='Project ID'
              >
                <Input
                  id='projectId'
                  {...register('projectId', {
                    required: 'Project ID is required.',
                  })}
                  placeholder='Project ID'
                  type='text'
                />
              </Field>

              <Field
                invalid={!!errors.assignedMemberId}
                errorText={errors.assignedMemberId?.message}
                label='Assigned Member ID'
              >
                <Input
                  id='assignedMemberId'
                  {...register('assignedMemberId')}
                  placeholder='Assigned Member ID'
                  type='text'
                />
              </Field>

              <Field
                required
                invalid={!!errors.status}
                errorText={errors.status?.message}
                label='Status'
              >
              <Input
                id='status'
                {...register('status')}
                placeholder='status'
                type='text'
              />
              </Field>
            </VStack>
          </DialogBody>

          <DialogFooter gap={2}>
            <DialogActionTrigger asChild>
              <Button
                variant='subtle'
                colorPalette='gray'
                disabled={isSubmitting}
              >
                Cancel
              </Button>
            </DialogActionTrigger>
            <Button
              variant='solid'
              type='submit'
              disabled={!isValid}
              loading={isSubmitting}
            >
              Save
            </Button>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  );
};

export default AddTask;
