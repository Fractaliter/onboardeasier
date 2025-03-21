import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"
import type { ProjectPublic } from "@/client"
import DeleteProject from "../Admin/DeleteProject"
import EditProject from "../Admin/EditProject"

interface ProjectActionsMenuProps {
  project: ProjectPublic
}

export const ProjectActionsMenu = ({ project}: ProjectActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditProject project={project} />
        <DeleteProject id={project.id} />
      </MenuContent>
    </MenuRoot>
  )
}
