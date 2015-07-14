// Generated by CoffeeScript 1.9.0
(function() {
  var VEL, camVel;

  VEL = 0.2;

  camVel = new THREE.Vector3(0, 0, 0);

  this.moveCamera = function() {
    return this.camera.position.add(camVel);
  };

  this.render = function() {
    return window.renderer.render(scene, camera);
  };

  this.animate = function() {
    requestAnimationFrame(animate);
    this.controls.update();
    return render();
  };

  this.init = function() {
    var axisHelper, container, radius;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    window.renderer = new THREE.WebGLRenderer({
      'antialias': false
    });
    renderer.setSize(window.innerWidth * 0.6, window.innerHeight * 0.6);
    renderer.setClearColor(0xeeeeee);
    this.drone = new THREE.Object3D();
    this.loader = new THREE.ColladaLoader();
    loader.load('assets/ar-drone-2.dae', function(result) {
      result.scene.scale.divideScalar(200);
      drone.add(result.scene);
      return render();
    });
    scene.add(drone);
    axisHelper = new THREE.AxisHelper(1.5);
    drone.add(axisHelper);
    axisHelper = new THREE.AxisHelper(4);
    scene.add(axisHelper);
    camera.position.y = -5;
    camera.position.z = 2;
    camera.up.set(0, 0.5, 1);
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    scene.add(camera);
    renderer.domElement.setAttribute("id", "main-canvas");
    container = document.getElementById('canvas-wrapper');
    container.appendChild(renderer.domElement);
    radius = 60;
    this.controls = new THREE.TrackballControls(camera, container);
    controls.rotateSpeed = 5;
    controls.zoomSpeed = 5;
    controls.panSpeed = 1;
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.3;
    controls.keys = [65, 83, 68];
    return controls.addEventListener('change', render);
  };

  this.updateStatus = function(status) {
    var ori, pos, statusdiv, theta, x, y;
    statusdiv = document.getElementById('status');
    pos = new THREE.Vector3().fromArray(status.pos);
    statusdiv.innerHTML = "(" + pos.x + ", " + pos.y + ", " + pos.z + ")";
    ori = new THREE.Matrix4();
    ori.set(status.ori[0], status.ori[1], status.ori[2], 0, status.ori[3], status.ori[4], status.ori[5], 0, status.ori[6], status.ori[7], status.ori[8], 0, 0, 0, 0, 1);
    theta = new THREE.Euler();
    theta.setFromRotationMatrix(ori);
    x = (new Date()).getTime();
    if (window.lastx === void 0 || window.lastx < x - 80) {
      y = theta._z;
      series.addPoint([x, y], true, false);
      window.lastx = x;
    }
    drone.position.copy(pos);
    return drone.rotation.setFromRotationMatrix(ori);
  };

  init();

  animate();

}).call(this);
