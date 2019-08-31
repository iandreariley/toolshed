# ToolShed Requirements

## Edit History
- Ian Riley 8/31/2019

## Requirements
- CLI
- Store scripts
- Remove scripts
- Edit scripts
- Run scripts
  - Must execute in current directory
  - Must take arguments
- Query scripts
  - Query by name or by tag
- Tags
  - Create tags
  - Query tags
  - Delete tags
    - Note, this should include an "are you sure" dialogue if any
    scripts currently use the tag. This dialogue should display the
    scripts that use the tag.
  - Tag when storing script
  - Tagging behavior:
    - Tags are not created by default - adding an unknown tag will give 
    an error. The intention is to keep users from accidentally creating
    new similar tags (e.g. "image" and "imaging" probably don't have
    much semantic difference when it comes to differentiating between
    scripts. A nice-to-have would be something that suggests similar
    tags to the user upon failure (a la git)
    - The above behavior can be overwritten by passing a flag (so that
    any unknown tags are created automatically and applied to the
    script)
- Query current location

## Nice-to-haves
- Tab completion of tags
- List of scripts using a tag when asked to delete