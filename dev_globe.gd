extends MeshInstance3D

@export var marker: PackedScene
var rng = RandomNumberGenerator.new()
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	
func get_rand_point():
	var r = mesh.radius
	var az = rng.randf_range(0, 2*PI)
	var colat = acos((2 * rng.randf_range(0, 0.5)) - 1 )
	
	return Vector3(
		r * sin(colat) * cos(az),
		r * cos(colat),
		r * sin(colat) * sin(az)
		
	)

func add_marker(pos):
	var inst = marker.instantiate()
	add_child(inst)
	inst.position = pos
