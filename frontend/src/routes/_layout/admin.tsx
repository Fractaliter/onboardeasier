import { Container, Heading } from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod";
import { useState } from "react";
import AddUser from "@/components/Admin/AddUser";
import AddProject from "@/components/Admin/AddProject";
import UsersTable from "@/components/Admin/UsersTable";
import ProjectsTable from "@/components/Admin/ProjectsTable";

// Define schema for query params
const searchSchema = z.object({
  userPage: z.number().default(1),
  projectPage: z.number().default(1),
});

export const Route = createFileRoute("/_layout/admin")({
  component: Admin,
  validateSearch: (search) => searchSchema.parse(search),
});

// -------- ADMIN PANEL --------
function Admin() {
  const { userPage, projectPage } = Route.useSearch();
  const [currentUserPage, setCurrentUserPage] = useState(userPage);
  const [currentProjectPage, setCurrentProjectPage] = useState(projectPage);

  return (
    <Container maxW="full">
      {/* Users Management */}
      <Heading size="lg" pt={12}>
        Users Management
      </Heading>
      <AddUser />
      <UsersTable
        userPage={currentUserPage}
        setUserPage={setCurrentUserPage}
      />

      {/* Projects Management */}
      <Heading size="lg" pt={12}>
        Project Management
      </Heading>
      <AddProject />
      <ProjectsTable
        projectPage={currentProjectPage}
        setProjectPage={setCurrentProjectPage}
      />
    </Container>
  );
}
