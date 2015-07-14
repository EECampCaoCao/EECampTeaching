
VEL = 0.2
camVel = new THREE.Vector3(0, 0, 0)
@moveCamera = () ->
  @camera.position.add camVel

@render = () ->
  window.renderer.render(scene, camera)

@animate = () ->
  requestAnimationFrame(animate)
  @controls.update()
  render()

@init = () ->
  @scene = new THREE.Scene()
  @camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000)

  @renderer = new THREE.WebGLRenderer({'antialias': false})
  renderer.setSize(window.innerWidth*0.6, window.innerHeight*0.6)
  renderer.setClearColor(0xeeeeee)

  @drone = new THREE.Object3D()
  @loader = new THREE.ColladaLoader()

  loader.load('assets/ar-drone-2.dae', (result) ->
    result.scene.scale.divideScalar(200)
    drone.add(result.scene)
    render()
  )
  scene.add(drone)
  axisHelper = new THREE.AxisHelper(1.5)
  drone.add(axisHelper)
  axisHelper = new THREE.AxisHelper(4)
  scene.add(axisHelper)

  camera.position.y = -5
  camera.position.z = 2
  camera.up.set(0, 0.5, 1)
  camera.lookAt(new THREE.Vector3(0, 0, 0))
  scene.add(camera)

  renderer.domElement.setAttribute("id", "main-canvas")
  container = document.getElementById('canvas-wrapper')
  container.appendChild(renderer.domElement)

  radius = 60
  @controls = new THREE.TrackballControls(camera, container)
  controls.rotateSpeed = 5
  controls.zoomSpeed = 5
  controls.panSpeed = 1
  controls.noZoom = false
  controls.noPan = false
  controls.staticMoving = true
  controls.dynamicDampingFactor = 0.3
  controls.keys = [65, 83, 68] # [ rotateKey, zoomKey, panKey ]
  controls.addEventListener('change', render)


@updateStatus = (status) ->
  statusdiv = document.getElementById('status')
  pos = new THREE.Vector3().fromArray(status.pos)
  statusdiv.innerHTML = "(" + pos.x + ", " + pos.y + ", " + pos.z + ")"
  ori = new THREE.Matrix4()
  ori.set(
    status.ori[0], status.ori[1], status.ori[2], 0,
    status.ori[3], status.ori[4], status.ori[5], 0,
    status.ori[6], status.ori[7], status.ori[8], 0,
    0, 0, 0, 1
  )
  theta = new THREE.Euler()
  theta.setFromRotationMatrix(ori)
  x = (new Date()).getTime() # current time
  if (window.lastx == undefined || window.lastx < x - 80) 
    y = theta._z
    series.addPoint([x, y], true, false)
    window.lastx = x

  drone.position.copy(pos)
  drone.rotation.setFromRotationMatrix(ori)

init()
animate()
