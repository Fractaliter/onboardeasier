import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"
import type { TaskPublic } from "@/client"

interface TaskActionsMenuProps {
  task: TaskPublic;
}

export const TaskActionsMenu = ({ }: TaskActionsMenuProps) => {
    return (
        <MenuRoot>
          <MenuTrigger asChild>
            <IconButton variant="ghost" color="inherit">
              <BsThreeDotsVertical />
            </IconButton>
          </MenuTrigger>
          <MenuContent>
            <IconButton variant="ghost" color="inherit">
              Edit
            </IconButton>
            <IconButton variant="ghost" color="inherit">
              Delete
            </IconButton>
          </MenuContent>
        </MenuRoot>
      )
}
