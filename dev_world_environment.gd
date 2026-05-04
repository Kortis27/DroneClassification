extends WorldEnvironment


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var image = Image.load_from_file("res://assets/backgrounds/grasslands_sunset_4k.exr")
	var texture = ImageTexture.create_from_image(image)
	
	environment.sky.sky_material.set_panorama(texture)
	
	#set_environment(environment)
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	var image = Image.load_from_file("res://assets/backgrounds/minedump_flats_4k.exr")
	var texture = ImageTexture.create_from_image(image)
	
	environment.sky.sky_material.set_panorama(texture)
