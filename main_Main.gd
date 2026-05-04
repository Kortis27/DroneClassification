extends Node3D

@export var object: PackedScene
@export var background: CompressedTexture2D

var rng = RandomNumberGenerator.new()
var label = 'burden'
var save_path = r"E:\Documents\AICapstoneData\dataset4\val" + '\\' + label
var n_pictures = 1000
var n_pictures_taken = 0
var background_paths = []
var model_paths = []
var backgrounds = []
var models = []
var offset = 0


func _ready() -> void:
	#ensure dataset dir is set up properly
	assert(DirAccess.dir_exists_absolute(save_path), 'Provided dataset path doesnt exist %s' % save_path)
	
	#fill background_paths
	background_paths = dir_contents('res://assets/backgrounds/').filter(func(f): return !f.ends_with(".import"))
	print(background_paths)
	#fill model_paths
	model_paths = dir_contents('res://assets/classes/' + label + '/').filter(func(f): return !f.ends_with(".import"))
	print(model_paths)
	
	#load objs
	#model_paths = ['box_burden.tscn', 'soda_can.tscn']
	for p in model_paths:
		var scene_resource: PackedScene = load('res://assets/classes/' + label + '/' + p) # Load the file
		var scene_instance: Node3D = scene_resource.instantiate() # Create the node
		models.append(scene_instance)
		scene_instance.hide()
		add_child(scene_instance) # Add to the game world

	#load background images
	for path in background_paths:
		var image = Image.load_from_file(r'res://assets/backgrounds/' + path)
		var texture = ImageTexture.create_from_image(image)
		backgrounds.append(texture)

	#set initial background
	##var texture = ImageTexture.create_from_image(image)
	$WorldEnvironment.environment.sky.sky_material.set_panorama(background)
	#add offet for images already taken
	var dir = DirAccess.open(save_path)
	for f in dir.get_files():
		offset += 1
	n_pictures += offset
	n_pictures_taken += offset
	
	RenderingServer.frame_post_draw.connect(_on_frame_rendered)
	
	
	
	
	#put all models in an array
	
	
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	
	#var image = Image.load_from_file(r'res://assets/backgrounds/' + backgrounds[i])
	#var texture = ImageTexture.create_from_image(image)
	
	if n_pictures_taken <= n_pictures:
		$WorldEnvironment.environment.sky.sky_material.set_panorama(backgrounds[n_pictures_taken % len(backgrounds)])
		models[n_pictures_taken % len(models)].show()
		
	
	
			
	
		
		

func get_rand_point():
	#var r = 800
	var r = rng.randf_range(5, 10)
	var az = rng.randf_range(0, 2*PI)
	var colat = acos((2 * rng.randf_range(0, 1)) - 1 )
	
	return Vector3(
		r * sin(colat) * cos(az),
		r * cos(colat),
		r * sin(colat) * sin(az)
		
	)

func _on_frame_rendered():
	# This runs AFTER the GPU has finished drawing the frame
	var obj_inst: Node3D = models[n_pictures_taken % len(models)]
	obj_inst.hide()
	if n_pictures_taken < n_pictures:
		obj_inst.set_rotation(Vector3(rng.randf_range(-(PI / 4), PI / 4),0,rng.randf_range(-(PI / 4), PI / 4)))
		$Camera3D.look_at_from_position(get_rand_point(), obj_inst.position)
		var fail = await $Camera3D.screenshot(save_path, r'\%s.png' % (n_pictures_taken + 1))
		if not fail:
			n_pictures_taken += 1
			print('took picture:' + r'\%s.png' % n_pictures_taken)
			
		else:
			print('Error')
			
func dir_contents(path):
	var dir = DirAccess.open(path)
	var fnames = []
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			fnames.append(file_name)
			file_name = dir.get_next()
		return fnames
	else:
		print("An error occurred when trying to access the path.")
		
