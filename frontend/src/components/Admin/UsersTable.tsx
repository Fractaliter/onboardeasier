// UsersTable.tsx
import { Badge, Flex, Table } from "@chakra-ui/react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
//import { useNavigate } from "@tanstack/react-router";
import { UserPublic, UsersService } from "@/client";
import { UserActionsMenu } from "@/components/Common/UserActionsMenu";
import PendingUsers from "@/components/Pending/PendingUsers";
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination";

const PER_PAGE = 5;

function getUsersQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      UsersService.readUsers({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
    queryKey: ["users", { page }],
  };
}

interface UsersTableProps {
  userPage: number;
  setUserPage: (page: number) => void;
}

const UsersTable: React.FC<UsersTableProps> = ({ userPage, setUserPage }) => {
  const queryClient = useQueryClient();
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"]);

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getUsersQueryOptions({ page: userPage }),
    placeholderData: (prevData) => prevData,
  });
  console.log('UsersTable rendered with userPage:', userPage);

  const users = data?.data.slice(0, PER_PAGE) ?? [];
  const count = data?.count ?? 0;

  if (isLoading) return <PendingUsers />;

  return (
    <>
      <Table.Root size={{ base: "sm", md: "md" }}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader w="sm">Full Name</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Email</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Role</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Status</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {users.map((user) => (
            <Table.Row key={user.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell>
                {user.full_name || "N/A"}
                {currentUser?.id === user.id && (
                  <Badge ml="1" colorScheme="teal">
                    You
                  </Badge>
                )}
              </Table.Cell>
              <Table.Cell>{user.email}</Table.Cell>
              <Table.Cell>{user.is_superuser ? "Superuser" : "User"}</Table.Cell>
              <Table.Cell>{user.is_active ? "Active" : "Inactive"}</Table.Cell>
              <Table.Cell>
                <UserActionsMenu
                  user={user}
                  disabled={currentUser?.id === user.id}
                />
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justifyContent="flex-end" mt={4}>
        <PaginationRoot
          count={count}
          pageSize={PER_PAGE}
          onPageChange={({ page }) => setUserPage(page)}
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

export default UsersTable;
