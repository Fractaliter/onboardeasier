import { Flex, Table } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { TasksService } from '@/client';
import { TaskActionsMenu } from '@/components/Common/TaskActionsMenu';
import PendingTasks from '@/components/Pending/PendingTasks';
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from '@/components/ui/pagination';

const PER_PAGE = 5;

function getTasksQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      TasksService.readTasks({
        skip: (page - 1) * PER_PAGE,
        limit: PER_PAGE,
      }),
    queryKey: ['tasks', { page }],
  };
}

interface TasksTableProps {
  taskPage: number;
  setTaskPage: (page: number) => void;
}

const TasksTable: React.FC<TasksTableProps> = ({ taskPage, setTaskPage }) => {
  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getTasksQueryOptions({ page: taskPage }),
    placeholderData: (prevData) => prevData,
  });

  const tasks = data?.data ?? [];
  const count = data?.count ?? 0;

  if (isLoading) return <PendingTasks />;

  return (
    <>
      <Table.Root size={{ base: 'sm', md: 'md' }}>
        <Table.Header>
          <Table.Row>
          <Table.ColumnHeader w="sm">Project</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Description</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Title</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Status</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Assigned Member</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {tasks.map((task) => (
            <Table.Row key={task.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell>{task.projectId}</Table.Cell>
              <Table.Cell>{task.description}</Table.Cell>
              <Table.Cell>{task.title}</Table.Cell>
              <Table.Cell>{task.status}</Table.Cell>
              <Table.Cell>{task.assignedMemberId || 'Unassigned'}</Table.Cell>
              <Table.Cell>
                <TaskActionsMenu task={task} />
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justifyContent="flex-end" mt={4}>
        <PaginationRoot
          count={count}
          pageSize={PER_PAGE}
          onPageChange={({ page }) => setTaskPage(page)}
        >
          <Flex>
            <PaginationPrevTrigger />
            <PaginationItems />
            <PaginationNextTrigger />
          </Flex>
        </PaginationRoot>
      </Flex>
    </>
  );
};

export default TasksTable;