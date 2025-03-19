import { Table } from "@chakra-ui/react"
import { SkeletonText } from "../ui/skeleton"

const PendingProjects = () => (
  <Table.Root size={{ base: "sm", md: "md" }}>
    <Table.Header>
    <Table.ColumnHeader w="sm">Pending Project name</Table.ColumnHeader>
    </Table.Header>
    <Table.Body>
        <Table.Row key={1}>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
        </Table.Row>
    </Table.Body>
  </Table.Root>
)

export default PendingProjects
