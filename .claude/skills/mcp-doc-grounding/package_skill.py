import os
import zipfile
from pathlib import Path

def package_skill():
    """Package the mcp-doc-grounding skill into a distributable zip file."""

    skill_name = "mcp-doc-grounding"
    skill_dir = Path(".") / ".claude" / "skills" / skill_name
    output_dir = skill_dir / "dist"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Define the output zip file
    zip_path = output_dir / f"{skill_name}.skill"

    # Create the zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_dir):
            # Skip the dist directory to avoid including the output in the package
            dirs[:] = [d for d in dirs if d != 'dist']

            for file in files:
                file_path = Path(root) / file
                # Calculate the relative path from skill_dir
                rel_path = file_path.relative_to(skill_dir.parent.parent)

                # Add file to zip with relative path
                zipf.write(file_path, rel_path)

    print(f"Skill packaged successfully as {zip_path}")

if __name__ == "__main__":
    package_skill()