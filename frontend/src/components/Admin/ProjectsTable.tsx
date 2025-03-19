// ProjectsTable.tsx
import { Flex, Table } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { ProjectsService } from "@/client";
import { ProjectActionsMenu } from "@/components/Common/ProjectActionsMenu";
import PendingProjects from "@/components/Pending/PendingProjects";
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination";

const PER_PAGE = 5;

function getProjectsQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      ProjectsService.readProjects({
        skip: (page - 1) * PER_PAGE,
        limit: PER_PAGE,
      }),
    queryKey: ["projects", { page }],
  };
}

interface ProjectsTableProps {
  projectPage: number;
  setProjectPage: (page: number) => void;
}

const ProjectsTable: React.FC<ProjectsTableProps> = ({
  projectPage,
  setProjectPage,
}) => {

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getProjectsQueryOptions({ page: projectPage }),
    placeholderData: (prevData) => prevData,
  });

  const projects = data?.data ?? [];
  const count = data?.count ?? 0;

  if (isLoading) return <PendingProjects />;

  return (
    <>
      <Table.Root size={{ base: "sm", md: "md" }}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader w="sm">Project Name</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Description</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Owner</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {projects.map((project) => (
            <Table.Row key={project.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell>{project.name}</Table.Cell>
              <Table.Cell>{project.description || "N/A"}</Table.Cell>
              <Table.Cell>{project.owner_id}</Table.Cell>
              <Table.Cell>
                <ProjectActionsMenu project={project} />
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justifyContent="flex-end" mt={4}>
        <PaginationRoot
          count={count}
          pageSize={PER_PAGE}
          onPageChange={({ page }) => setProjectPage(page)}
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

export default ProjectsTable;
