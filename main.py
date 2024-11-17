import numpy as np
from stl import mesh
import pickle

def load_from_pickle(fname,scale):
    points = pickle.load(open(f"{fname}.pkl","rb"))
    points = points*scale
    return points

def generate_vertices(points,thickness):
    points_count=len(points)
    vertex_count = points_count**2
    v_upper = np.zeros((vertex_count,3))
    v_lower = np.zeros((vertex_count,3))
    for i in range(points_count):
        for j in range(points_count):
            idx = j + (points_count*i)
            v_upper[idx] = [j,i,points[i][j]]
            v_lower[idx] = [j,i,points[i][j]-thickness]
    vertices = []
    vertices.extend(v_upper)
    vertices.extend(v_lower)
    return vertices

def generate_faces(vertices,points_count):
    f_upper = []
    f_lower = []
    f_sides = []
    for i in range(points_count):
        for j in range(points_count):
            idx = j + (points_count*i)
            # generate top and bottom faces
            if j < points_count-1 and i < points_count-1:
                f_upper.append([idx,idx+1,idx+points_count+1])
                f_upper.append([idx,idx+points_count+1,idx+points_count])
                f_lower.append([idx+points_count**2,idx+points_count+1+points_count**2,idx+1+points_count**2])
                f_lower.append([idx+points_count**2,idx+points_count+points_count**2,idx+points_count+1+points_count**2])
            # generate side faces
            if i == 0 and j != points_count-1:
                f_sides.append([idx,idx+points_count**2,idx+1+points_count**2])
                f_sides.append([idx,idx+1,idx+1+points_count**2])
            if i == points_count-1 and j != points_count-1:
                f_sides.append([idx,idx+1+points_count**2,idx+points_count**2])
                f_sides.append([idx,idx+1+points_count**2,idx+1])
            if j == 0 and i != points_count-1:
                f_sides.append([idx,idx+points_count**2,idx+points_count+points_count**2])
                f_sides.append([idx,idx+points_count,idx+points_count+points_count**2])
            if j == points_count-1 and i != points_count-1:
                f_sides.append([idx,idx+points_count+points_count**2,idx+points_count**2])
                f_sides.append([idx,idx+points_count+points_count**2,idx+points_count])
    faces = []
    faces.extend(f_upper)
    faces.extend(f_lower)
    faces.extend(f_sides)
    return faces

def build_mesh(faces,vertices,fname):
    faces = np.asarray(faces)
    wvfn_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i,f in enumerate(faces):
        for j in range(3):
            wvfn_mesh.vectors[i][j] = vertices[f[j]][:]
    wvfn_mesh.save(f"{fname}.stl")
    



def run(fname,scale=300,thickness=12):
    points = load_from_pickle(fname,scale)
    vertices = generate_vertices(points,thickness)
    faces = generate_faces(vertices,len(points))
    build_mesh(faces,vertices,fname)

run("double_excitation_real")