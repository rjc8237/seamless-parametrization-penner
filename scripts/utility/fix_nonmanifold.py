

import pymeshlab as pml
import igl
import numpy as np
import os, multiprocessing
import pandas as pd


def process_mesh(m):
	def check_topo(ms):
			top = ms.get_topological_measures()
			print('non manifold edges: ',top['non_two_manifold_edges'])
			print('non manifold vertices: ',top['non_two_manifold_vertices'])
			return top 

	name=str(m)
	data_dir = './data/tetwild_10k_surface'
	output_dir = './data/tetwild_nonmanifold'

	print('processing {}'.format(name))
	ms = pml.MeshSet()
	ms.load_new_mesh(os.path.join(data_dir, name + "_sf.obj"))
	top= check_topo(ms)
	print('removing non-manifold edges')
	ms.compute_selection_by_non_manifold_edges_per_face()
	ms.meshing_remove_selected_vertices_and_faces()
	top = check_topo(ms)

	print('removing non-manifold vertices')
	while top['non_two_manifold_vertices'] != 0: 
			ms.compute_selection_by_non_manifold_per_vertex()
			ms.meshing_remove_selected_vertices_and_faces()
			top = check_topo(ms)

	print('filling holes (igl)')
	vF = ms.mesh(0).face_matrix().copy()
	vV =  ms.mesh(0).vertex_matrix().copy()
	l = igl.boundary_loop(vF)
	vp = np.array([[0.,0.,0.]])
	print(len(vF))
	while len(l) > 0:
			print('loop len:', len(l))
			vp = np.array([[0.,0.,0.]])
			for v in l:
					vp = vp + np.array([vV[v,:]])
			vp = vp/len(l)
			vF = igl.topological_hole_fill(vF, [l])
			vV = np.append(vV,vp,axis=0)
			l = igl.boundary_loop(vF)

	print('worst triangle quality in/circumradius*2:',  2*(igl.inradius(vV,vF)/igl.circumradius(vV,vF)).min())

	# assuming  name.type
	newname = name + '_nonmanifold_cleaned.obj'
	igl.write_obj(os.path.join(output_dir, newname),vV,vF)

if __name__ == "__main__":
	output_dir = './data/tetwild_nonmanifold'
	print('Writing meshes to {}'.format(output_dir))
	os.makedirs(output_dir, exist_ok=True)
	df = pd.read_csv('./data/mesh_stats_thingi10k_tetwild.csv')
	nonmanifold = df.loc[~df['is_mesh_two_manifold']]['id'].to_numpy()
	print('{} nonmanifold meshes'.format(len(nonmanifold)))

	with multiprocessing.Pool(processes=8) as pool:
			all_mesh_info = pool.map(process_mesh, nonmanifold, chunksize=1)
