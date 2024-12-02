from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import subprocess
import os

class IDEExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, WorkspaceOpener())

class WorkspaceOpener(EventListener):
    def get_search_paths(self, paths_string):
        # Split paths by comma and expand home directory
        paths = [os.path.expanduser(path.strip()) for path in paths_string.split(',')]
        return [path for path in paths if os.path.exists(path)]

    def get_editor_icon(self, editor):
        # Map of editor names to their icon files
        icon_mapping = {
            'code': 'code.png',
            'cursor': 'cursor.png',
            'windsurf': 'windsurf.svg',
        }
        
        icon_path = f"images/{icon_mapping.get(editor, 'default.svg')}"
        return icon_path if os.path.exists(icon_path) else 'images/default.svg'

    def on_event(self, event, extension):
        search_paths = self.get_search_paths(extension.preferences['paths'])
        query = event.get_argument() or ""
        
        # Parse editor from query if specified (e.g., "code:myproject" or "windsurf:myproject")
        editor = extension.preferences['default_editor']
        search_term = query
        
        if query and ':' in query:
            parts = query.split(':', 1)
            # Check if first part matches any editor option
            possible_editor = parts[0].lower()
            if possible_editor in ['code', 'subl', 'atom', 'vim', 'nvim', 'emacs', 'kate', 'cursor', 'windsurf']:
                editor = possible_editor
                search_term = parts[1] if len(parts) > 1 else ""
            
        items = []
        for base_path in search_paths:
            try:
                # Find git repositories in each search path
                cmd = f"find {base_path} -type d -name .git -prune -exec dirname {{}} \;"
                if search_term:
                    cmd += f" | grep -i {search_term}"
                
                output = subprocess.check_output(cmd, shell=True, text=True)
                projects = output.splitlines()

                # Add found projects to results
                for project in projects:
                    items.append(
                        ExtensionResultItem(
                            icon=self.get_editor_icon(editor),
                            name=f"[{editor}] {os.path.basename(project)}",
                            description=project,
                            on_enter=RunScriptAction(
                                f"{editor} {project}"
                            )
                        )
                    )

                # Limit results to top 10
                if len(items) >= 10:
                    break

            except subprocess.CalledProcessError:
                continue

        # If no results found, show a message
        if not items:
            items.append(
                ExtensionResultItem(
                    icon='images/default.svg',
                    name='No workspaces found',
                    description='No matching workspaces found in the specified paths',
                    on_enter=HideWindowAction()
                )
            )

        return RenderResultListAction(items[:10])

if __name__ == '__main__':
    IDEExtension().run()