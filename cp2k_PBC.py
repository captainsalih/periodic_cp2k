#VARIABLE
input_file_name = "md.traj_0.xyz"
output_file_name = "PBC.xyz"
box = [21.4, 21.4, 21.4]

def apply_pbc(coord, box):
    return [coord[i] % box[i] for i in range(3)]

def wrap_coordinates(input_path, output_path, box):
    frame_count = 0
    with open(input_path, "r") as input_file, open(output_path, "w") as output_file:
        lines_buffer = []
        for line in input_file:
            lines_buffer.append(line.strip())

            if len(lines_buffer) == 1:
                try:
                    num_particles = int(lines_buffer[0])
                    frame_line_count = num_particles + 2
                except ValueError:
                    print(f"Warning: Cannot parse atom count in frame {frame_count}")
                    lines_buffer = []
                    continue

            if len(lines_buffer) == frame_line_count:
                atom_count_line = lines_buffer[0]
                comment_line = lines_buffer[1]
                atom_lines = lines_buffer[2:]

                output_file.write(f"{atom_count_line}\n")
                output_file.write(f"{comment_line}\n")

                for atom_line in atom_lines:
                    parts = atom_line.split()
                    if len(parts) < 4:
                        continue
                    atom = parts[0]
                    coords = list(map(float, parts[1:4]))
                    wrapped_coords = apply_pbc(coords, box)
                    output_file.write(f"{atom}  {wrapped_coords[0]:.6f} {wrapped_coords[1]:.6f} {wrapped_coords[2]:.6f}\n")

                lines_buffer = []
                frame_count += 1

    print("PBC wrapping completed. Output saved as", output_file_name)
    print("Number of frames processed:", frame_count)

# EXECUTION
wrap_coordinates(input_file_name, output_file_name, box)

