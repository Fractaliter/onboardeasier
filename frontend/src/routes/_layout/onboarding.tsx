import {
    Container,
    Heading,
  } from "@chakra-ui/react"
  import { createFileRoute} from "@tanstack/react-router"
import { z } from "zod"
import { useState } from "react";
import AddProject from "@/components/Admin/AddProject";
import TasksTable from "@/components/Onboarding/TasksTable";
import AddTask from "@/components/Onboarding/AddTask";
import ProjectsTable from "@/components/Admin/ProjectsTable";

const tasksSearchSchema = z.object({
    page: z.number().catch(1),
    projectPage: z.number().default(1),
    taskPage: z.number().default(1),
  })
  
  export const Route = createFileRoute("/_layout/onboarding")({
    component: Onboarding,
    validateSearch: (search) => tasksSearchSchema.parse(search),
  })

  // -------- ADMIN PANEL --------
function Onboarding() {
  const {projectPage, taskPage } = Route.useSearch();
  const [currentProjectPage, setCurrentProjectPage] = useState(projectPage);
  const [currentTaskPage, setCurrentTaskPage] = useState(taskPage);
    return (
      <Container maxW="full">
        <Heading size="lg" pt={12}>
        Project Management
      </Heading>
      <AddProject />
      <ProjectsTable
        projectPage={currentProjectPage}
        setProjectPage={setCurrentProjectPage}
      />
        {/* Task Management */}
        <Heading size="lg" pt={12}>
          Task Management
        </Heading>
        <AddTask />
      <TasksTable 
        taskPage={currentTaskPage}
        setTaskPage={setCurrentTaskPage
         }/>
      </Container>
    );
  }
  