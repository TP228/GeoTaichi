def stl_to_obj(stl_path, obj_path):
    """
    Converts an ASCII STL file to a Wavefront OBJ file.
    Extracts unique vertices and triangular face indices from the STL data.
    """
    vert_to_idx = {}    # Map from (x, y, z) tuple to unique vertex index
    vertices = []       # List of unique vertex coordinates
    faces = []          # List of triangular face indices (as vertex index tuples)

    with open(stl_path, 'r') as f:
        current_face = []
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'vertex' and len(parts) >= 4:
                x, y, z = map(float, parts[1:4])
                coord = (x, y, z)

                if coord not in vert_to_idx:
                    vert_to_idx[coord] = len(vertices)
                    vertices.append(coord)

                current_face.append(vert_to_idx[coord])

                if len(current_face) == 3:
                    faces.append(tuple(current_face))
                    current_face = []

    with open(obj_path, 'w') as out:
        out.write(f"# Converted from '{stl_path}'\n")
        out.write(f"# vertex count = {len(vertices)}\n")
        out.write(f"# face count = {len(faces)}\n")
        for (x, y, z) in vertices:
            out.write(f"v {x} {y} {z}\n")
        for (i0, i1, i2) in faces:
            out.write(f"f {i0+1} {i1+1} {i2+1}\n")


if __name__ == "__main__":
    input_stl = "input.stl"
    output_obj = "output.obj"
    stl_to_obj(input_stl, output_obj)
    print(f"'{input_stl}' → '{output_obj}' conversion complete.")
