root = window.App

class Scene
  constructor: () ->

  init: () ->
    @scene = new THREE.Scene()

    wrapper = $ '#canvas-wrapper'
    [w, h] = [wrapper.width(), wrapper.height()]
    @camera = new THREE.PerspectiveCamera(75, w/h, 0.1, 1000)

    @renderer = new THREE.WebGLRenderer({'antialias': false})
    @renderer.setSize w, h
    @renderer.setClearColor(0xeeeeee)

    @drone = new THREE.Object3D()
    @loader = new THREE.ColladaLoader()

    @loader.load('assets/ar-drone-2.dae', (result) =>
      result.scene.scale.divideScalar(200)
      @drone.add(result.scene)
      @render()
    )
    @scene.add(@drone)
    axisHelper = new THREE.AxisHelper(1.5)
    @drone.add(axisHelper)
    axisHelper = new THREE.AxisHelper(4)
    @scene.add(axisHelper)

    light1 = new THREE.PointLight 0xffffff, 6, 200
    light1.position.set 0, 0, 100
    light2 = new THREE.PointLight 0xffffff, 3, 200
    light2.position.set 0, 0, -100
    @scene.add light1
    @scene.add light2

    @camera.position.y = -5
    @camera.position.z = 2
    @camera.up.set(0, 0.5, 1)
    @camera.lookAt(new THREE.Vector3(0, 0, 0))
    @scene.add(@camera)

    @renderer.domElement.setAttribute("id", "main-canvas")
    container = document.getElementById('canvas-wrapper')
    container.appendChild(@renderer.domElement)

    radius = 60
    @controls = new THREE.TrackballControls(@camera, container)
    @controls.rotateSpeed = 5
    @controls.zoomSpeed = 5
    @controls.panSpeed = 1
    @controls.noZoom = false
    @controls.noPan = false
    @controls.staticMoving = true
    @controls.dynamicDampingFactor = 0.3
    @controls.keys = [65, 83, 68] # [ rotateKey, zoomKey, panKey ]
    @controls.addEventListener('change', @render)


  updateStatus: (status) ->
    #statusdiv = document.getElementById('status')
    pos = new THREE.Vector3().fromArray(status.pos)
    #statusdiv.innerHTML = "(" + pos.x + ", " + pos.y + ", " + pos.z + ")"
    ori = new THREE.Matrix4()
    ori.set(
      status.ori[0], status.ori[1], status.ori[2], 0,
      status.ori[3], status.ori[4], status.ori[5], 0,
      status.ori[6], status.ori[7], status.ori[8], 0,
      0, 0, 0, 1
    )
    motor = status.motor
    t = (new Date()) # current time
    if (@lastUpdateTime == undefined || 
        t.getTime() - @lastUpdateTime > 50) 
      #flag = root.series.data.length > 100
      #root.series.addPoint([x, y], true, flag)
      theta = new THREE.Euler()
      theta.setFromRotationMatrix(ori)
      root.updateChart t, [theta._x, theta._y, theta._z, 
                           motor[0], motor[1], motor[2], motor[3]]
      @lastUpdateTime = t.getTime()

    @drone.position.copy(pos)
    @drone.rotation.setFromRotationMatrix(ori)

  render: () =>
    @renderer.render(@scene, @camera)

  animate: () =>
    requestAnimationFrame(@animate)
    @controls.update()
    @render()

  start: () ->
    @init()
    @animate()

root.scene = new Scene()
