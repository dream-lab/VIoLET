(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{C1df:function(t,e,n){"use strict";n.d(e,"a",function(){return o});var i=new(function(){function t(){}return t.prototype.getAllStyles=function(t){return window.getComputedStyle(t)},t.prototype.getStyle=function(t,e){return this.getAllStyles(t)[e]},t.prototype.isStaticPositioned=function(t){return"static"===(this.getStyle(t,"position")||"static")},t.prototype.offsetParent=function(t){for(var e=t.offsetParent||document.documentElement;e&&e!==document.documentElement&&this.isStaticPositioned(e);)e=e.offsetParent;return e||document.documentElement},t.prototype.position=function(t,e){var n;void 0===e&&(e=!0);var i={width:0,height:0,top:0,bottom:0,left:0,right:0};if("fixed"===this.getStyle(t,"position"))n=t.getBoundingClientRect();else{var o=this.offsetParent(t);n=this.offset(t,!1),o!==document.documentElement&&(i=this.offset(o,!1)),i.top+=o.clientTop,i.left+=o.clientLeft}return n.top-=i.top,n.bottom-=i.top,n.left-=i.left,n.right-=i.left,e&&(n.top=Math.round(n.top),n.bottom=Math.round(n.bottom),n.left=Math.round(n.left),n.right=Math.round(n.right)),n},t.prototype.offset=function(t,e){void 0===e&&(e=!0);var n=t.getBoundingClientRect(),i=window.pageYOffset-document.documentElement.clientTop,o=window.pageXOffset-document.documentElement.clientLeft,r={height:n.height||t.offsetHeight,width:n.width||t.offsetWidth,top:n.top+i,bottom:n.bottom+i,left:n.left+o,right:n.right+o};return e&&(r.height=Math.round(r.height),r.width=Math.round(r.width),r.top=Math.round(r.top),r.bottom=Math.round(r.bottom),r.left=Math.round(r.left),r.right=Math.round(r.right)),r},t.prototype.positionElements=function(t,e,n,i){var o=i?this.offset(t,!1):this.position(t,!1),r=this.getAllStyles(e),s=e.getBoundingClientRect(),u=n.split("-")[0]||"top",p=n.split("-")[1]||"center",a={height:s.height||e.offsetHeight,width:s.width||e.offsetWidth,top:0,bottom:s.height||e.offsetHeight,left:0,right:s.width||e.offsetWidth};switch(u){case"top":a.top=o.top-(e.offsetHeight+parseFloat(r.marginBottom));break;case"bottom":a.top=o.top+o.height;break;case"left":a.left=o.left-(e.offsetWidth+parseFloat(r.marginRight));break;case"right":a.left=o.left+o.width}switch(p){case"top":a.top=o.top;break;case"bottom":a.top=o.top+o.height-e.offsetHeight;break;case"left":a.left=o.left;break;case"right":a.left=o.left+o.width-e.offsetWidth;break;case"center":"top"===u||"bottom"===u?a.left=o.left+o.width/2-e.offsetWidth/2:a.top=o.top+o.height/2-e.offsetHeight/2}return a.top=Math.round(a.top),a.bottom=Math.round(a.bottom),a.left=Math.round(a.left),a.right=Math.round(a.right),a},t.prototype.getAvailablePlacements=function(t,e){var n=[],i=t.getBoundingClientRect(),o=e.getBoundingClientRect(),r=document.documentElement,s=window.innerHeight||r.clientHeight,u=window.innerWidth||r.clientWidth,p=i.left+i.width/2,a=i.top+i.height/2;return o.width<i.left&&(a>o.height/2&&s-a>o.height/2&&n.splice(n.length,1,"left"),this.setSecondaryPlacementForLeftRight(i,o,"left",n)),o.height<i.top&&(p>o.width/2&&u-p>o.width/2&&n.splice(n.length,1,"top"),this.setSecondaryPlacementForTopBottom(i,o,"top",n)),u-i.right>o.width&&(a>o.height/2&&s-a>o.height/2&&n.splice(n.length,1,"right"),this.setSecondaryPlacementForLeftRight(i,o,"right",n)),s-i.bottom>o.height&&(p>o.width/2&&u-p>o.width/2&&n.splice(n.length,1,"bottom"),this.setSecondaryPlacementForTopBottom(i,o,"bottom",n)),n},t.prototype.setSecondaryPlacementForLeftRight=function(t,e,n,i){var o=document.documentElement;e.height<=t.bottom&&i.splice(i.length,1,n+"-bottom"),(window.innerHeight||o.clientHeight)-t.top>=e.height&&i.splice(i.length,1,n+"-top")},t.prototype.setSecondaryPlacementForTopBottom=function(t,e,n,i){var o=document.documentElement;(window.innerWidth||o.clientWidth)-t.left>=e.width&&i.splice(i.length,1,n+"-left"),e.width<=t.right&&i.splice(i.length,1,n+"-right")},t}());function o(t,e,n,o){var r=Array.isArray(n)?n:[n],s=r.findIndex(function(t){return"auto"===t});s>=0&&["top","bottom","left","right","top-left","top-right","bottom-left","bottom-right","left-top","left-bottom","right-top","right-bottom"].forEach(function(t){null==r.find(function(e){return-1!==e.search("^"+t)})&&r.splice(s++,1,t)});for(var u,p=0,a=0,c=i.getAvailablePlacements(t,e),h=function(n,s){if(null!=c.find(function(t){return t===n})||r.length===s+1){u=n;var h=i.positionElements(t,e,n,o);return p=h.top,a=h.left,"break"}},f=0,l=r.map(function(t,e){return{item:t,index:e}});f<l.length;f++){var m=l[f];if("break"===h(m.item,m.index))break}return e.style.top=p+"px",e.style.left=a+"px",u}},C9m0:function(t,e,n){"use strict";var i,o=n("CcnG"),r=n("mrSG"),s=n("isby"),u=n("IUTb"),p=n("MGBS"),a=n("zotm"),c=function(){function t(){}return t.prototype.call=function(t,e){return e.subscribe(new h(t))},t}(),h=function(t){function e(e){var n=t.call(this,e)||this;return n.hasFirst=!1,n.observables=[],n.subscriptions=[],n}return r.b(e,t),e.prototype._next=function(t){this.observables.push(t)},e.prototype._complete=function(){var t=this.observables,e=t.length;if(0===e)this.destination.complete();else{for(var n=0;n<e&&!this.hasFirst;n++){var i=t[n],o=Object(a.a)(this,i,i,n);this.subscriptions&&this.subscriptions.push(o),this.add(o)}this.observables=null}},e.prototype.notifyNext=function(t,e,n,i,o){if(!this.hasFirst){this.hasFirst=!0;for(var r=0;r<this.subscriptions.length;r++)if(r!==n){var s=this.subscriptions[r];s.unsubscribe(),this.remove(s)}this.subscriptions=null}this.destination.next(e)},e}(p.a),f=n("K9Ia"),l=n("bne5"),m=n("ny24"),d=n("VnD/"),y=n("ebCm"),_=n("C1df"),g=n("ldgc"),v=(i=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var n in e)e.hasOwnProperty(n)&&(t[n]=e[n])},function(t,e){function n(){this.constructor=t}i(t,e),t.prototype=null===e?Object.create(e):(n.prototype=e.prototype,new n)}),b=function(){function t(t,e,n){this.dropdown=t,this._elementRef=e,this._renderer=n,this.placement="bottom",this.isOpen=!1}return t.prototype.isEventFrom=function(t){return this._elementRef.nativeElement.contains(t.target)},t.prototype.position=function(t,e){this.applyPlacement(Object(_.a)(t,this._elementRef.nativeElement,e))},t.prototype.applyPlacement=function(t){this._renderer.removeClass(this._elementRef.nativeElement.parentNode,"dropup"),this._renderer.removeClass(this._elementRef.nativeElement.parentNode,"dropdown"),this.placement=t,-1!==t.search("^top")?this._renderer.addClass(this._elementRef.nativeElement.parentNode,"dropup"):this._renderer.addClass(this._elementRef.nativeElement.parentNode,"dropdown")},t}(),w=function(t){function e(e,n){return t.call(this,e,n)||this}return v(e,t),e.prototype.toggleOpen=function(){this.dropdown.toggle()},e}(function(){function t(t,e){this.dropdown=t,this._elementRef=e,this.anchorEl=e.nativeElement}return t.prototype.isEventFrom=function(t){return this._elementRef.nativeElement.contains(t.target)},t}()),I=function(){function t(t,e,n,i){var r=this;this._changeDetector=t,this._document=n,this._ngZone=i,this._closed$=new f.a,this._open=!1,this.openChange=new o.m,this.placement=e.placement,this.autoClose=e.autoClose,this._zoneSubscription=i.onStable.subscribe(function(){r._positionMenu()})}return t.prototype.ngOnInit=function(){this._menu&&this._menu.applyPlacement(Array.isArray(this.placement)?this.placement[0]:this.placement),this._open&&this._setCloseHandlers()},t.prototype.isOpen=function(){return this._open},t.prototype.open=function(){this._open||(this._open=!0,this._positionMenu(),this.openChange.emit(!0),this._setCloseHandlers())},t.prototype._setCloseHandlers=function(){var t=this;this.autoClose&&this._ngZone.runOutsideAngular(function(){(function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];if(1===t.length){if(!Object(s.a)(t[0]))return t[0];t=t[0]}return Object(u.a)(t,void 0).lift(new c)})([Object(l.a)(t._document,"keyup").pipe(Object(m.a)(t._closed$),Object(d.a)(function(t){return t.which===g.a.Escape})),Object(l.a)(t._document,"click").pipe(Object(m.a)(t._closed$),Object(d.a)(function(e){return t._shouldCloseFromClick(e)}))]).pipe(Object(m.a)(t._closed$)).subscribe(function(){return t._ngZone.run(function(){t.close(),t._changeDetector.markForCheck()})})})},t.prototype.close=function(){this._open&&(this._open=!1,this._closed$.next(),this.openChange.emit(!1))},t.prototype.toggle=function(){this.isOpen()?this.close():this.open()},t.prototype._shouldCloseFromClick=function(t){if(2!==t.button&&!this._isEventFromToggle(t)){if(!0===this.autoClose)return!0;if("inside"===this.autoClose&&this._isEventFromMenu(t))return!0;if("outside"===this.autoClose&&!this._isEventFromMenu(t))return!0}return!1},t.prototype.ngOnDestroy=function(){this._closed$.next(),this._zoneSubscription.unsubscribe()},t.prototype._isEventFromToggle=function(t){return this._anchor.isEventFrom(t)},t.prototype._isEventFromMenu=function(t){return!!this._menu&&this._menu.isEventFrom(t)},t.prototype._positionMenu=function(){this.isOpen()&&this._menu&&this._menu.position(this._anchor.anchorEl,this.placement)},t}();n.d(e,"a",function(){return j}),n.d(e,!1,function(){return I}),n.d(e,!1,function(){return w}),n.d(e,!1,function(){return b}),n.d(e,!1,function(){return y.a});var j=function(){function t(){}return t.forRoot=function(){return{ngModule:t,providers:[y.a]}},t}()},bne5:function(t,e,n){"use strict";n.d(e,"a",function(){return u});var i=n("6blF"),o=n("isby"),r=n("2Bdj"),s=n("67Y/");function u(t,e,n,p){return Object(r.a)(n)&&(p=n,n=void 0),p?u(t,e,n).pipe(Object(s.a)(function(t){return Object(o.a)(t)?p.apply(void 0,t):p(t)})):new i.a(function(i){!function t(e,n,i,o,r){var s;if(function(t){return t&&"function"==typeof t.addEventListener&&"function"==typeof t.removeEventListener}(e)){var u=e;e.addEventListener(n,i,r),s=function(){return u.removeEventListener(n,i,r)}}else if(function(t){return t&&"function"==typeof t.on&&"function"==typeof t.off}(e)){var p=e;e.on(n,i),s=function(){return p.off(n,i)}}else if(function(t){return t&&"function"==typeof t.addListener&&"function"==typeof t.removeListener}(e)){var a=e;e.addListener(n,i),s=function(){return a.removeListener(n,i)}}else{if(!e||!e.length)throw new TypeError("Invalid event target");for(var c=0,h=e.length;c<h;c++)t(e[c],n,i,o,r)}o.add(s)}(t,e,function(t){i.next(arguments.length>1?Array.prototype.slice.call(arguments):t)},i,n)})}Object},ebCm:function(t,e,n){"use strict";n.d(e,"a",function(){return i});var i=function(){this.autoClose=!0,this.placement="bottom-left"}},ldgc:function(t,e,n){"use strict";n.d(e,"a",function(){return i});var i=function(t){return t[t.Tab=9]="Tab",t[t.Enter=13]="Enter",t[t.Escape=27]="Escape",t[t.Space=32]="Space",t[t.PageUp=33]="PageUp",t[t.PageDown=34]="PageDown",t[t.End=35]="End",t[t.Home=36]="Home",t[t.ArrowLeft=37]="ArrowLeft",t[t.ArrowUp=38]="ArrowUp",t[t.ArrowRight=39]="ArrowRight",t[t.ArrowDown=40]="ArrowDown",t}({})},ny24:function(t,e,n){"use strict";n.d(e,"a",function(){return s});var i=n("mrSG"),o=n("MGBS"),r=n("zotm");function s(t){return function(e){return e.lift(new u(t))}}var u=function(){function t(t){this.notifier=t}return t.prototype.call=function(t,e){var n=new p(t),i=Object(r.a)(n,this.notifier);return i&&!i.closed?(n.add(i),e.subscribe(n)):n},t}(),p=function(t){function e(e){return t.call(this,e)||this}return i.b(e,t),e.prototype.notifyNext=function(t,e,n,i,o){this.complete()},e.prototype.notifyComplete=function(){},e}(o.a)},vw6C:function(t,e,n){"use strict";n.d(e,"a",function(){return r});var i=n("CcnG"),o=n("t/Na"),r=function(){function t(t){this.http=t,this.url="http://"+window.location.hostname+":5000/",this.files={},this.images={},this.inputFileDD={},this.outputFileDD={},this.consoleOutput={},this.summaryInfraInput={},this.summaryInfraOutput={},this.inputInfraFile="",this.outputInfraFile="",this.generateInfraStatus="",this.summaryPartitionInput={},this.summaryPartitionOutput={},this.inputPartitionFile="",this.outputPartitionFile="",this.partitionStatus="",this.inputDepFile="",this.outputDepFile="",this.deploymentStatus="success",this.inputSanFile="",this.outputSanFile="",this.sanityStatus="success"}return t.prototype.getSummaryInfraInput=function(){var t=JSON.parse(this.files["infra_gen.json"]),e=JSON.parse(this.files["device_types.json"]);for(var n in this.summaryInfraInput.pvt_networks=Object.keys(t.private_networks).length,this.summaryInfraInput.pub_networks=Object.keys(t.public_networks).length,this.summaryInfraInput.pvt_bandwidth=t.network.private_networks.bandwidth_mbps.join(", "),this.summaryInfraInput.pub_bandwidth=t.network.public_networks.bandwidth_mbps.join(", "),this.summaryInfraInput.pvt_latency=t.network.private_networks.latency_ms.join(", "),this.summaryInfraInput.pub_latency=t.network.public_networks.latency_ms.join(", "),this.summaryInfraInput.pvt_dev_cnt=0,this.summaryInfraInput.pvt_dev={},this.summaryInfraInput.pub_dev={},this.summaryInfraInput.dev_cnt=1,e)this.summaryInfraInput.pvt_dev[n]=0,this.summaryInfraInput.pub_dev[n]=0,this.summaryInfraInput.dev_cnt+=1;for(var n in t.private_networks)this.summaryInfraInput.pvt_dev_cnt+=+t.private_networks[n].number_devices+1,this.summaryInfraInput.pvt_dev[t.private_networks[n].device_type]+=+t.private_networks[n].number_devices+1;for(var n in this.summaryInfraInput.pub_dev_cnt=0,t.public_networks)for(var i=0,o=t.public_networks[n];i<o.length;i++){var r=o[i];this.summaryInfraInput.pub_dev_cnt+=+r.number_devices,this.summaryInfraInput.pub_dev[r.device_type]+=+r.number_devices}},t.prototype.getSummaryInfraOutput=function(){var t=JSON.parse(this.files["infra_config.json"]),e=JSON.parse(this.files["infra_gen.json"]),n=JSON.parse(this.files["device_types.json"]);for(var i in this.summaryInfraOutput.pvt=t.private_networks,this.summaryInfraOutput.pub=t.public_networks,this.summaryInfraOutput.pvt_dev={},this.summaryInfraOutput.pub_dev={},e.private_networks)for(var o in this.summaryInfraOutput.pvt_dev[i]={},n)this.summaryInfraOutput.pvt_dev[i][o]=o===e.private_networks[i].device_type?+e.private_networks[i].number_devices+1:0;for(var i in e.public_networks){for(var r in this.summaryInfraOutput.pub_dev[i]={},n)this.summaryInfraOutput.pub_dev[i][r]=0;for(var s=0,u=e.public_networks[i];s<u.length;s++)this.summaryInfraOutput.pub_dev[i][(o=u[s]).device_type]=+o.number_devices}},t.prototype.getInfraInput=function(){var t=this;this.http.get(this.url+"infra_gen_input").subscribe(function(e){t.files["infra_gen.json"]=e["infra_gen.json"],t.files["device_types.json"]=e["device_types.json"],t.inputFileDD.infra=["infra_gen.json"],t.inputInfraFile=t.inputFileDD.infra[0],t.getSummaryInfraInput()})},t.prototype.getInfraOutput=function(){var t=this;this.http.get(this.url+"infra_gen_output").subscribe(function(e){t.files["infra_config.json"]=e.data,t.outputFileDD.infra=["infra_config.json"],t.outputInfraFile=t.outputFileDD.infra[0],t.getSummaryInfraOutput()})},t.prototype.getSummaryPartitionInput=function(){for(var t in this.summaryPartitionInput.vmc=JSON.parse(this.files["vm_config.json"]),this.summaryPartitionInput.vmt=JSON.parse(this.files["vm_types.json"]),this.summaryPartitionInput.dvt=JSON.parse(this.files["device_types.json"]),this.summaryPartitionInput.vm_count=Object.keys(this.summaryPartitionInput.vmc.container_VM).length,this.summaryPartitionInput.used={},this.summaryPartitionInput.vmt)this.summaryPartitionInput.used[t]=0;for(var t in this.summaryPartitionInput.vmc.container_VM)this.summaryPartitionInput.used[this.summaryPartitionInput.vmc.container_VM[t].vm_type]=1;console.log(this.summaryPartitionInput.used)},t.prototype.getSummaryPartitionOutput=function(){var t=this,e=JSON.parse(this.files["metis_partitions.json"]),n=0;for(var i in this.summaryPartitionOutput.cnt={},Object.entries(this.summaryPartitionInput.vmc.container_VM).forEach(function(e){var i=e[0];t.summaryPartitionOutput.cnt[n.toString()]={name:i,cnt:0},n++}),e)this.summaryPartitionOutput.cnt[e[i]].cnt++},t.prototype.getPartitionPlots=function(){var t=this;this.http.get(this.url+"partition_plot_coremark",{responseType:"blob"}).subscribe(function(e){t.createImageFromBlob(e,"partition_coremark"),t.http.get(t.url+"partition_plot_disk",{responseType:"blob"}).subscribe(function(e){t.createImageFromBlob(e,"partition_disk"),t.http.get(t.url+"partition_plot_memory",{responseType:"blob"}).subscribe(function(e){t.createImageFromBlob(e,"partition_memory")})})})},t.prototype.getPartitionInput=function(){var t=this;this.http.get(this.url+"partition_input").subscribe(function(e){t.files["vm_config.json"]=e["vm_config.json"],t.files["vm_types.json"]=e["vm_types.json"],t.inputFileDD.partition=["vm_types.json","vm_config.json","device_types.json"],t.inputPartitionFile=t.inputFileDD.partition[0],t.getSummaryPartitionInput()})},t.prototype.getPartitionOutput=function(){var t=this;this.http.get(this.url+"partition_output").subscribe(function(e){t.files["metis_partitions.json"]=e["metis_partitions.json"],t.outputFileDD.partition=["metis_partitions.json"],t.outputPartitionFile=t.outputFileDD.partition[0],t.getSummaryPartitionOutput()})},t.prototype.getDeploymentInput=function(){var t=this;this.http.get(this.url+"deployment_input").subscribe(function(e){t.files["deployment.json"]=e["deployment.json"],t.files["sensor_types.json"]=e["sensor_types.json"],t.inputFileDD.deployment=["infra_config.json","vm_types.json","device_types.json","vm_config.json","metis_partitions.json","deployment.json","sensor_types.json"],t.inputDepFile=t.inputFileDD.deployment[0]})},t.prototype.getDeploymentOutput=function(){var t=this;this.http.get(this.url+"deployment_output").subscribe(function(e){t.files["deployment_output.json"]=e["deployment_output.json"],t.outputFileDD.deployment=["deployment_output.json"],t.outputDepFile=t.outputFileDD.deployment[0]})},t.prototype.getDeploymentPlots=function(){var t=this;this.http.get(this.url+"deployment_plot",{responseType:"blob"}).subscribe(function(e){t.createImageFromBlob(e,"deployment_network")})},t.prototype.createImageFromBlob=function(t,e){var n=this,i=new FileReader;i.addEventListener("load",function(){n.images[e]=i.result},!1),t&&i.readAsDataURL(t)},t.prototype.getSanityInput=function(){this.inputFileDD.sanity=["infra_config.json","vm_config.json","metis_partitions.json","deployment.json","sensor_types.json"],this.inputSanFile=this.inputFileDD.sanity[0]},t.prototype.getSanityCPUPlots=function(){var t=this;this.http.get(this.url+"sanity_cpu_plots",{responseType:"blob"}).subscribe(function(e){t.createImageFromBlob(e,"cpu_plot")})},t.ngInjectableDef=i.Q({factory:function(){return new t(i.U(o.c))},token:t,providedIn:"root"}),t}()}}]);