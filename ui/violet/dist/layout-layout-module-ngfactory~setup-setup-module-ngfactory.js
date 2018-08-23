(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["layout-layout-module-ngfactory~setup-setup-module-ngfactory"],{

/***/ "./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown-config.js":
/*!*****************************************************************************!*\
  !*** ./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown-config.js ***!
  \*****************************************************************************/
/*! exports provided: NgbDropdownConfig */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownConfig", function() { return NgbDropdownConfig; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");

/**
 * Configuration service for the NgbDropdown directive.
 * You can inject this service, typically in your root component, and customize the values of its properties in
 * order to provide default values for all the dropdowns used in the application.
 */
var NgbDropdownConfig = /** @class */ (function () {
    function NgbDropdownConfig() {
        this.autoClose = true;
        this.placement = 'bottom-left';
    }
    NgbDropdownConfig.decorators = [
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"] },
    ];
    return NgbDropdownConfig;
}());

//# sourceMappingURL=dropdown-config.js.map

/***/ }),

/***/ "./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown.js":
/*!**********************************************************************!*\
  !*** ./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown.js ***!
  \**********************************************************************/
/*! exports provided: NgbDropdownMenu, NgbDropdownAnchor, NgbDropdownToggle, NgbDropdown */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownMenu", function() { return NgbDropdownMenu; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownAnchor", function() { return NgbDropdownAnchor; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownToggle", function() { return NgbDropdownToggle; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NgbDropdown", function() { return NgbDropdown; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _dropdown_config__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dropdown-config */ "./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown-config.js");
/* harmony import */ var _util_positioning__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../util/positioning */ "./node_modules/@ng-bootstrap/ng-bootstrap/util/positioning.js");
/* harmony import */ var _util_key__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../util/key */ "./node_modules/@ng-bootstrap/ng-bootstrap/util/key.js");
var __extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();







/**
 */
var NgbDropdownMenu = /** @class */ (function () {
    function NgbDropdownMenu(dropdown, _elementRef, _renderer) {
        this.dropdown = dropdown;
        this._elementRef = _elementRef;
        this._renderer = _renderer;
        this.placement = 'bottom';
        this.isOpen = false;
    }
    NgbDropdownMenu.prototype.isEventFrom = function ($event) { return this._elementRef.nativeElement.contains($event.target); };
    NgbDropdownMenu.prototype.position = function (triggerEl, placement) {
        this.applyPlacement(Object(_util_positioning__WEBPACK_IMPORTED_MODULE_5__["positionElements"])(triggerEl, this._elementRef.nativeElement, placement));
    };
    NgbDropdownMenu.prototype.applyPlacement = function (_placement) {
        // remove the current placement classes
        this._renderer.removeClass(this._elementRef.nativeElement.parentNode, 'dropup');
        this._renderer.removeClass(this._elementRef.nativeElement.parentNode, 'dropdown');
        this.placement = _placement;
        /**
             * apply the new placement
             * in case of top use up-arrow or down-arrow otherwise
             */
        if (_placement.search('^top') !== -1) {
            this._renderer.addClass(this._elementRef.nativeElement.parentNode, 'dropup');
        }
        else {
            this._renderer.addClass(this._elementRef.nativeElement.parentNode, 'dropdown');
        }
    };
    NgbDropdownMenu.decorators = [
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"], args: [{
                    selector: '[ngbDropdownMenu]',
                    host: { '[class.dropdown-menu]': 'true', '[class.show]': 'dropdown.isOpen()', '[attr.x-placement]': 'placement' }
                },] },
    ];
    /** @nocollapse */
    NgbDropdownMenu.ctorParameters = function () { return [
        { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"], args: [Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["forwardRef"])(function () { return NgbDropdown; }),] },] },
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"], },
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Renderer2"], },
    ]; };
    return NgbDropdownMenu;
}());

/**
 * Marks an element to which dropdown menu will be anchored. This is a simple version
 * of the NgbDropdownToggle directive. It plays the same role as NgbDropdownToggle but
 * doesn't listen to click events to toggle dropdown menu thus enabling support for
 * events other than click.
 *
 * @since 1.1.0
 */
var NgbDropdownAnchor = /** @class */ (function () {
    function NgbDropdownAnchor(dropdown, _elementRef) {
        this.dropdown = dropdown;
        this._elementRef = _elementRef;
        this.anchorEl = _elementRef.nativeElement;
    }
    NgbDropdownAnchor.prototype.isEventFrom = function ($event) { return this._elementRef.nativeElement.contains($event.target); };
    NgbDropdownAnchor.decorators = [
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"], args: [{
                    selector: '[ngbDropdownAnchor]',
                    host: { 'class': 'dropdown-toggle', 'aria-haspopup': 'true', '[attr.aria-expanded]': 'dropdown.isOpen()' }
                },] },
    ];
    /** @nocollapse */
    NgbDropdownAnchor.ctorParameters = function () { return [
        { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"], args: [Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["forwardRef"])(function () { return NgbDropdown; }),] },] },
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"], },
    ]; };
    return NgbDropdownAnchor;
}());

/**
 * Allows the dropdown to be toggled via click. This directive is optional: you can use NgbDropdownAnchor as an
 * alternative.
 */
var NgbDropdownToggle = /** @class */ (function (_super) {
    __extends(NgbDropdownToggle, _super);
    function NgbDropdownToggle(dropdown, elementRef) {
        return _super.call(this, dropdown, elementRef) || this;
    }
    NgbDropdownToggle.prototype.toggleOpen = function () { this.dropdown.toggle(); };
    NgbDropdownToggle.decorators = [
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"], args: [{
                    selector: '[ngbDropdownToggle]',
                    host: {
                        'class': 'dropdown-toggle',
                        'aria-haspopup': 'true',
                        '[attr.aria-expanded]': 'dropdown.isOpen()',
                        '(click)': 'toggleOpen()'
                    },
                    providers: [{ provide: NgbDropdownAnchor, useExisting: Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["forwardRef"])(function () { return NgbDropdownToggle; }) }]
                },] },
    ];
    /** @nocollapse */
    NgbDropdownToggle.ctorParameters = function () { return [
        { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"], args: [Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["forwardRef"])(function () { return NgbDropdown; }),] },] },
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"], },
    ]; };
    return NgbDropdownToggle;
}(NgbDropdownAnchor));

/**
 * Transforms a node into a dropdown.
 */
var NgbDropdown = /** @class */ (function () {
    function NgbDropdown(_changeDetector, config, _document, _ngZone) {
        var _this = this;
        this._changeDetector = _changeDetector;
        this._document = _document;
        this._ngZone = _ngZone;
        this._closed$ = new rxjs__WEBPACK_IMPORTED_MODULE_2__["Subject"]();
        /**
           *  Defines whether or not the dropdown-menu is open initially.
           */
        this._open = false;
        /**
           *  An event fired when the dropdown is opened or closed.
           *  Event's payload equals whether dropdown is open.
           */
        this.openChange = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
        this.placement = config.placement;
        this.autoClose = config.autoClose;
        this._zoneSubscription = _ngZone.onStable.subscribe(function () { _this._positionMenu(); });
    }
    NgbDropdown.prototype.ngOnInit = function () {
        if (this._menu) {
            this._menu.applyPlacement(Array.isArray(this.placement) ? (this.placement[0]) : this.placement);
        }
        if (this._open) {
            this._setCloseHandlers();
        }
    };
    /**
     * Checks if the dropdown menu is open or not.
     */
    /**
       * Checks if the dropdown menu is open or not.
       */
    NgbDropdown.prototype.isOpen = /**
       * Checks if the dropdown menu is open or not.
       */
    function () { return this._open; };
    /**
     * Opens the dropdown menu of a given navbar or tabbed navigation.
     */
    /**
       * Opens the dropdown menu of a given navbar or tabbed navigation.
       */
    NgbDropdown.prototype.open = /**
       * Opens the dropdown menu of a given navbar or tabbed navigation.
       */
    function () {
        if (!this._open) {
            this._open = true;
            this._positionMenu();
            this.openChange.emit(true);
            this._setCloseHandlers();
        }
    };
    NgbDropdown.prototype._setCloseHandlers = function () {
        var _this = this;
        if (this.autoClose) {
            this._ngZone.runOutsideAngular(function () {
                var escapes$ = Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["fromEvent"])(_this._document, 'keyup')
                    .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(_this._closed$), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["filter"])(function (event) { return event.which === _util_key__WEBPACK_IMPORTED_MODULE_6__["Key"].Escape; }));
                var clicks$ = Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["fromEvent"])(_this._document, 'click')
                    .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(_this._closed$), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["filter"])(function (event) { return _this._shouldCloseFromClick(event); }));
                Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["race"])([escapes$, clicks$]).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(_this._closed$)).subscribe(function () {
                    return _this._ngZone.run(function () {
                        _this.close();
                        _this._changeDetector.markForCheck();
                    });
                });
            });
        }
    };
    /**
     * Closes the dropdown menu of a given navbar or tabbed navigation.
     */
    /**
       * Closes the dropdown menu of a given navbar or tabbed navigation.
       */
    NgbDropdown.prototype.close = /**
       * Closes the dropdown menu of a given navbar or tabbed navigation.
       */
    function () {
        if (this._open) {
            this._open = false;
            this._closed$.next();
            this.openChange.emit(false);
        }
    };
    /**
     * Toggles the dropdown menu of a given navbar or tabbed navigation.
     */
    /**
       * Toggles the dropdown menu of a given navbar or tabbed navigation.
       */
    NgbDropdown.prototype.toggle = /**
       * Toggles the dropdown menu of a given navbar or tabbed navigation.
       */
    function () {
        if (this.isOpen()) {
            this.close();
        }
        else {
            this.open();
        }
    };
    NgbDropdown.prototype._shouldCloseFromClick = function (event) {
        if (event.button !== 2 && !this._isEventFromToggle(event)) {
            if (this.autoClose === true) {
                return true;
            }
            else if (this.autoClose === 'inside' && this._isEventFromMenu(event)) {
                return true;
            }
            else if (this.autoClose === 'outside' && !this._isEventFromMenu(event)) {
                return true;
            }
        }
        return false;
    };
    NgbDropdown.prototype.ngOnDestroy = function () {
        this._closed$.next();
        this._zoneSubscription.unsubscribe();
    };
    NgbDropdown.prototype._isEventFromToggle = function ($event) { return this._anchor.isEventFrom($event); };
    NgbDropdown.prototype._isEventFromMenu = function ($event) { return this._menu ? this._menu.isEventFrom($event) : false; };
    NgbDropdown.prototype._positionMenu = function () {
        if (this.isOpen() && this._menu) {
            this._menu.position(this._anchor.anchorEl, this.placement);
        }
    };
    NgbDropdown.decorators = [
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"], args: [{ selector: '[ngbDropdown]', exportAs: 'ngbDropdown', host: { '[class.show]': 'isOpen()' } },] },
    ];
    /** @nocollapse */
    NgbDropdown.ctorParameters = function () { return [
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectorRef"], },
        { type: _dropdown_config__WEBPACK_IMPORTED_MODULE_4__["NgbDropdownConfig"], },
        { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"], args: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"],] },] },
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"], },
    ]; };
    NgbDropdown.propDecorators = {
        "_menu": [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ContentChild"], args: [NgbDropdownMenu,] },],
        "_anchor": [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ContentChild"], args: [NgbDropdownAnchor,] },],
        "autoClose": [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"] },],
        "_open": [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"], args: ['open',] },],
        "placement": [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"] },],
        "openChange": [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"] },],
    };
    return NgbDropdown;
}());

//# sourceMappingURL=dropdown.js.map

/***/ }),

/***/ "./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown.module.js":
/*!*****************************************************************************!*\
  !*** ./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown.module.js ***!
  \*****************************************************************************/
/*! exports provided: NgbDropdown, NgbDropdownToggle, NgbDropdownMenu, NgbDropdownConfig, NgbDropdownModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownModule", function() { return NgbDropdownModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _dropdown__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./dropdown */ "./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown.js");
/* harmony import */ var _dropdown_config__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./dropdown-config */ "./node_modules/@ng-bootstrap/ng-bootstrap/dropdown/dropdown-config.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "NgbDropdown", function() { return _dropdown__WEBPACK_IMPORTED_MODULE_1__["NgbDropdown"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownToggle", function() { return _dropdown__WEBPACK_IMPORTED_MODULE_1__["NgbDropdownToggle"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownMenu", function() { return _dropdown__WEBPACK_IMPORTED_MODULE_1__["NgbDropdownMenu"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "NgbDropdownConfig", function() { return _dropdown_config__WEBPACK_IMPORTED_MODULE_2__["NgbDropdownConfig"]; });






var NGB_DROPDOWN_DIRECTIVES = [_dropdown__WEBPACK_IMPORTED_MODULE_1__["NgbDropdown"], _dropdown__WEBPACK_IMPORTED_MODULE_1__["NgbDropdownAnchor"], _dropdown__WEBPACK_IMPORTED_MODULE_1__["NgbDropdownToggle"], _dropdown__WEBPACK_IMPORTED_MODULE_1__["NgbDropdownMenu"]];
var NgbDropdownModule = /** @class */ (function () {
    function NgbDropdownModule() {
    }
    NgbDropdownModule.forRoot = function () { return { ngModule: NgbDropdownModule, providers: [_dropdown_config__WEBPACK_IMPORTED_MODULE_2__["NgbDropdownConfig"]] }; };
    NgbDropdownModule.decorators = [
        { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"], args: [{ declarations: NGB_DROPDOWN_DIRECTIVES, exports: NGB_DROPDOWN_DIRECTIVES },] },
    ];
    return NgbDropdownModule;
}());

//# sourceMappingURL=dropdown.module.js.map

/***/ }),

/***/ "./node_modules/@ng-bootstrap/ng-bootstrap/util/key.js":
/*!*************************************************************!*\
  !*** ./node_modules/@ng-bootstrap/ng-bootstrap/util/key.js ***!
  \*************************************************************/
/*! exports provided: Key */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Key", function() { return Key; });
var Key;
(function (Key) {
    Key[Key["Tab"] = 9] = "Tab";
    Key[Key["Enter"] = 13] = "Enter";
    Key[Key["Escape"] = 27] = "Escape";
    Key[Key["Space"] = 32] = "Space";
    Key[Key["PageUp"] = 33] = "PageUp";
    Key[Key["PageDown"] = 34] = "PageDown";
    Key[Key["End"] = 35] = "End";
    Key[Key["Home"] = 36] = "Home";
    Key[Key["ArrowLeft"] = 37] = "ArrowLeft";
    Key[Key["ArrowUp"] = 38] = "ArrowUp";
    Key[Key["ArrowRight"] = 39] = "ArrowRight";
    Key[Key["ArrowDown"] = 40] = "ArrowDown";
})(Key || (Key = {}));
//# sourceMappingURL=key.js.map

/***/ }),

/***/ "./node_modules/@ng-bootstrap/ng-bootstrap/util/positioning.js":
/*!*********************************************************************!*\
  !*** ./node_modules/@ng-bootstrap/ng-bootstrap/util/positioning.js ***!
  \*********************************************************************/
/*! exports provided: Positioning, positionElements */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Positioning", function() { return Positioning; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "positionElements", function() { return positionElements; });
// previous version:
// https://github.com/angular-ui/bootstrap/blob/07c31d0731f7cb068a1932b8e01d2312b796b4ec/src/position/position.js
var 
// previous version:
// https://github.com/angular-ui/bootstrap/blob/07c31d0731f7cb068a1932b8e01d2312b796b4ec/src/position/position.js
Positioning = /** @class */ (function () {
    function Positioning() {
    }
    Positioning.prototype.getAllStyles = function (element) { return window.getComputedStyle(element); };
    Positioning.prototype.getStyle = function (element, prop) { return this.getAllStyles(element)[prop]; };
    Positioning.prototype.isStaticPositioned = function (element) {
        return (this.getStyle(element, 'position') || 'static') === 'static';
    };
    Positioning.prototype.offsetParent = function (element) {
        var offsetParentEl = element.offsetParent || document.documentElement;
        while (offsetParentEl && offsetParentEl !== document.documentElement && this.isStaticPositioned(offsetParentEl)) {
            offsetParentEl = offsetParentEl.offsetParent;
        }
        return offsetParentEl || document.documentElement;
    };
    Positioning.prototype.position = function (element, round) {
        if (round === void 0) { round = true; }
        var elPosition;
        var parentOffset = { width: 0, height: 0, top: 0, bottom: 0, left: 0, right: 0 };
        if (this.getStyle(element, 'position') === 'fixed') {
            elPosition = element.getBoundingClientRect();
        }
        else {
            var offsetParentEl = this.offsetParent(element);
            elPosition = this.offset(element, false);
            if (offsetParentEl !== document.documentElement) {
                parentOffset = this.offset(offsetParentEl, false);
            }
            parentOffset.top += offsetParentEl.clientTop;
            parentOffset.left += offsetParentEl.clientLeft;
        }
        elPosition.top -= parentOffset.top;
        elPosition.bottom -= parentOffset.top;
        elPosition.left -= parentOffset.left;
        elPosition.right -= parentOffset.left;
        if (round) {
            elPosition.top = Math.round(elPosition.top);
            elPosition.bottom = Math.round(elPosition.bottom);
            elPosition.left = Math.round(elPosition.left);
            elPosition.right = Math.round(elPosition.right);
        }
        return elPosition;
    };
    Positioning.prototype.offset = function (element, round) {
        if (round === void 0) { round = true; }
        var elBcr = element.getBoundingClientRect();
        var viewportOffset = {
            top: window.pageYOffset - document.documentElement.clientTop,
            left: window.pageXOffset - document.documentElement.clientLeft
        };
        var elOffset = {
            height: elBcr.height || element.offsetHeight,
            width: elBcr.width || element.offsetWidth,
            top: elBcr.top + viewportOffset.top,
            bottom: elBcr.bottom + viewportOffset.top,
            left: elBcr.left + viewportOffset.left,
            right: elBcr.right + viewportOffset.left
        };
        if (round) {
            elOffset.height = Math.round(elOffset.height);
            elOffset.width = Math.round(elOffset.width);
            elOffset.top = Math.round(elOffset.top);
            elOffset.bottom = Math.round(elOffset.bottom);
            elOffset.left = Math.round(elOffset.left);
            elOffset.right = Math.round(elOffset.right);
        }
        return elOffset;
    };
    Positioning.prototype.positionElements = function (hostElement, targetElement, placement, appendToBody) {
        var hostElPosition = appendToBody ? this.offset(hostElement, false) : this.position(hostElement, false);
        var targetElStyles = this.getAllStyles(targetElement);
        var targetElBCR = targetElement.getBoundingClientRect();
        var placementPrimary = placement.split('-')[0] || 'top';
        var placementSecondary = placement.split('-')[1] || 'center';
        var targetElPosition = {
            'height': targetElBCR.height || targetElement.offsetHeight,
            'width': targetElBCR.width || targetElement.offsetWidth,
            'top': 0,
            'bottom': targetElBCR.height || targetElement.offsetHeight,
            'left': 0,
            'right': targetElBCR.width || targetElement.offsetWidth
        };
        switch (placementPrimary) {
            case 'top':
                targetElPosition.top =
                    hostElPosition.top - (targetElement.offsetHeight + parseFloat(targetElStyles.marginBottom));
                break;
            case 'bottom':
                targetElPosition.top = hostElPosition.top + hostElPosition.height;
                break;
            case 'left':
                targetElPosition.left =
                    hostElPosition.left - (targetElement.offsetWidth + parseFloat(targetElStyles.marginRight));
                break;
            case 'right':
                targetElPosition.left = hostElPosition.left + hostElPosition.width;
                break;
        }
        switch (placementSecondary) {
            case 'top':
                targetElPosition.top = hostElPosition.top;
                break;
            case 'bottom':
                targetElPosition.top = hostElPosition.top + hostElPosition.height - targetElement.offsetHeight;
                break;
            case 'left':
                targetElPosition.left = hostElPosition.left;
                break;
            case 'right':
                targetElPosition.left = hostElPosition.left + hostElPosition.width - targetElement.offsetWidth;
                break;
            case 'center':
                if (placementPrimary === 'top' || placementPrimary === 'bottom') {
                    targetElPosition.left = hostElPosition.left + hostElPosition.width / 2 - targetElement.offsetWidth / 2;
                }
                else {
                    targetElPosition.top = hostElPosition.top + hostElPosition.height / 2 - targetElement.offsetHeight / 2;
                }
                break;
        }
        targetElPosition.top = Math.round(targetElPosition.top);
        targetElPosition.bottom = Math.round(targetElPosition.bottom);
        targetElPosition.left = Math.round(targetElPosition.left);
        targetElPosition.right = Math.round(targetElPosition.right);
        return targetElPosition;
    };
    // get the availble placements of the target element in the viewport dependeing on the host element
    // get the availble placements of the target element in the viewport dependeing on the host element
    Positioning.prototype.getAvailablePlacements = 
    // get the availble placements of the target element in the viewport dependeing on the host element
    function (hostElement, targetElement) {
        var availablePlacements = [];
        var hostElemClientRect = hostElement.getBoundingClientRect();
        var targetElemClientRect = targetElement.getBoundingClientRect();
        var html = document.documentElement;
        var windowHeight = window.innerHeight || html.clientHeight;
        var windowWidth = window.innerWidth || html.clientWidth;
        var hostElemClientRectHorCenter = hostElemClientRect.left + hostElemClientRect.width / 2;
        var hostElemClientRectVerCenter = hostElemClientRect.top + hostElemClientRect.height / 2;
        // left: check if target width can be placed between host left and viewport start and also height of target is
        // inside viewport
        if (targetElemClientRect.width < hostElemClientRect.left) {
            // check for left only
            if (hostElemClientRectVerCenter > targetElemClientRect.height / 2 &&
                windowHeight - hostElemClientRectVerCenter > targetElemClientRect.height / 2) {
                availablePlacements.splice(availablePlacements.length, 1, 'left');
            }
            // check for left-top and left-bottom
            this.setSecondaryPlacementForLeftRight(hostElemClientRect, targetElemClientRect, 'left', availablePlacements);
        }
        // top: target height is less than host top
        if (targetElemClientRect.height < hostElemClientRect.top) {
            if (hostElemClientRectHorCenter > targetElemClientRect.width / 2 &&
                windowWidth - hostElemClientRectHorCenter > targetElemClientRect.width / 2) {
                availablePlacements.splice(availablePlacements.length, 1, 'top');
            }
            this.setSecondaryPlacementForTopBottom(hostElemClientRect, targetElemClientRect, 'top', availablePlacements);
        }
        // right: check if target width can be placed between host right and viewport end and also height of target is
        // inside viewport
        if (windowWidth - hostElemClientRect.right > targetElemClientRect.width) {
            // check for right only
            if (hostElemClientRectVerCenter > targetElemClientRect.height / 2 &&
                windowHeight - hostElemClientRectVerCenter > targetElemClientRect.height / 2) {
                availablePlacements.splice(availablePlacements.length, 1, 'right');
            }
            // check for right-top and right-bottom
            this.setSecondaryPlacementForLeftRight(hostElemClientRect, targetElemClientRect, 'right', availablePlacements);
        }
        // bottom: check if there is enough space between host bottom and viewport end for target height
        if (windowHeight - hostElemClientRect.bottom > targetElemClientRect.height) {
            if (hostElemClientRectHorCenter > targetElemClientRect.width / 2 &&
                windowWidth - hostElemClientRectHorCenter > targetElemClientRect.width / 2) {
                availablePlacements.splice(availablePlacements.length, 1, 'bottom');
            }
            this.setSecondaryPlacementForTopBottom(hostElemClientRect, targetElemClientRect, 'bottom', availablePlacements);
        }
        return availablePlacements;
    };
    /**
     * check if secondary placement for left and right are available i.e. left-top, left-bottom, right-top, right-bottom
     * primaryplacement: left|right
     * availablePlacementArr: array in which available placemets to be set
     */
    /**
       * check if secondary placement for left and right are available i.e. left-top, left-bottom, right-top, right-bottom
       * primaryplacement: left|right
       * availablePlacementArr: array in which available placemets to be set
       */
    Positioning.prototype.setSecondaryPlacementForLeftRight = /**
       * check if secondary placement for left and right are available i.e. left-top, left-bottom, right-top, right-bottom
       * primaryplacement: left|right
       * availablePlacementArr: array in which available placemets to be set
       */
    function (hostElemClientRect, targetElemClientRect, primaryPlacement, availablePlacementArr) {
        var html = document.documentElement;
        // check for left-bottom
        if (targetElemClientRect.height <= hostElemClientRect.bottom) {
            availablePlacementArr.splice(availablePlacementArr.length, 1, primaryPlacement + '-bottom');
        }
        if ((window.innerHeight || html.clientHeight) - hostElemClientRect.top >= targetElemClientRect.height) {
            availablePlacementArr.splice(availablePlacementArr.length, 1, primaryPlacement + '-top');
        }
    };
    /**
     * check if secondary placement for top and bottom are available i.e. top-left, top-right, bottom-left, bottom-right
     * primaryplacement: top|bottom
     * availablePlacementArr: array in which available placemets to be set
     */
    /**
       * check if secondary placement for top and bottom are available i.e. top-left, top-right, bottom-left, bottom-right
       * primaryplacement: top|bottom
       * availablePlacementArr: array in which available placemets to be set
       */
    Positioning.prototype.setSecondaryPlacementForTopBottom = /**
       * check if secondary placement for top and bottom are available i.e. top-left, top-right, bottom-left, bottom-right
       * primaryplacement: top|bottom
       * availablePlacementArr: array in which available placemets to be set
       */
    function (hostElemClientRect, targetElemClientRect, primaryPlacement, availablePlacementArr) {
        var html = document.documentElement;
        // check for left-bottom
        if ((window.innerWidth || html.clientWidth) - hostElemClientRect.left >= targetElemClientRect.width) {
            availablePlacementArr.splice(availablePlacementArr.length, 1, primaryPlacement + '-left');
        }
        if (targetElemClientRect.width <= hostElemClientRect.right) {
            availablePlacementArr.splice(availablePlacementArr.length, 1, primaryPlacement + '-right');
        }
    };
    return Positioning;
}());
// previous version:
// https://github.com/angular-ui/bootstrap/blob/07c31d0731f7cb068a1932b8e01d2312b796b4ec/src/position/position.js

var positionService = new Positioning();
/*
 * Accept the placement array and applies the appropriate placement dependent on the viewport.
 * Returns the applied placement.
 * In case of auto placement, placements are selected in order
 *   'top', 'bottom', 'left', 'right',
 *   'top-left', 'top-right',
 *   'bottom-left', 'bottom-right',
 *   'left-top', 'left-bottom',
 *   'right-top', 'right-bottom'.
 * */
function positionElements(hostElement, targetElement, placement, appendToBody) {
    var placementVals = Array.isArray(placement) ? placement : [placement];
    // replace auto placement with other placements
    var hasAuto = placementVals.findIndex(function (val) { return val === 'auto'; });
    if (hasAuto >= 0) {
        ['top', 'bottom', 'left', 'right', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'left-top',
            'left-bottom', 'right-top', 'right-bottom',
        ].forEach(function (obj) {
            if (placementVals.find(function (val) { return val.search('^' + obj) !== -1; }) == null) {
                placementVals.splice(hasAuto++, 1, obj);
            }
        });
    }
    // coordinates where to position
    var topVal = 0, leftVal = 0;
    var appliedPlacement;
    // get available placements
    var availablePlacements = positionService.getAvailablePlacements(hostElement, targetElement);
    var _loop_1 = function (item, index) {
        // check if passed placement is present in the available placement or otherwise apply the last placement in the
        // passed placement list
        if ((availablePlacements.find(function (val) { return val === item; }) != null) || (placementVals.length === index + 1)) {
            appliedPlacement = item;
            var pos = positionService.positionElements(hostElement, targetElement, item, appendToBody);
            topVal = pos.top;
            leftVal = pos.left;
            return "break";
        }
    };
    // iterate over all the passed placements
    for (var _i = 0, _a = toItemIndexes(placementVals); _i < _a.length; _i++) {
        var _b = _a[_i], item = _b.item, index = _b.index;
        var state_1 = _loop_1(item, index);
        if (state_1 === "break")
            break;
    }
    targetElement.style.top = topVal + "px";
    targetElement.style.left = leftVal + "px";
    return appliedPlacement;
}
// function to get index and item of an array
function toItemIndexes(a) {
    return a.map(function (item, index) { return ({ item: item, index: index }); });
}
//# sourceMappingURL=positioning.js.map

/***/ }),

/***/ "./src/app/layout/setup/setup-data.service.ts":
/*!****************************************************!*\
  !*** ./src/app/layout/setup/setup-data.service.ts ***!
  \****************************************************/
/*! exports provided: SetupDataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SetupDataService", function() { return SetupDataService; });
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");



var SetupDataService = /** @class */ (function () {
    function SetupDataService(http) {
        this.http = http;
        this.url = 'http://' + window.location.hostname + ':5000/';
        this.files = {};
        this.images = {};
        this.inputFileDD = {};
        this.outputFileDD = {};
        this.consoleOutput = {};
        this.summaryInfraInput = {};
        this.summaryInfraOutput = {};
        this.inputInfraFile = '';
        this.outputInfraFile = '';
        this.generateInfraStatus = '';
        this.summaryPartitionInput = {};
        this.summaryPartitionOutput = {};
        this.inputPartitionFile = '';
        this.outputPartitionFile = '';
        this.partitionStatus = '';
        this.inputDepFile = '';
        this.outputDepFile = '';
        this.deploymentStatus = '';
        this.inputSanFile = '';
        this.outputSanFile = '';
        this.sanityStatus = '';
    }
    // Infra
    SetupDataService.prototype.getSummaryInfraInput = function () {
        var temp = JSON.parse(this.files['infra_gen.json']);
        var temp1 = JSON.parse(this.files['device_types.json']);
        this.summaryInfraInput['pvt_networks'] = Object.keys(temp.private_networks).length;
        this.summaryInfraInput['pub_networks'] = Object.keys(temp.public_networks).length;
        this.summaryInfraInput['pvt_bandwidth'] = temp.network.private_networks.bandwidth_mbps.join(', ');
        this.summaryInfraInput['pub_bandwidth'] = temp.network.public_networks.bandwidth_mbps.join(', ');
        this.summaryInfraInput['pvt_latency'] = temp.network.private_networks.latency_ms.join(', ');
        this.summaryInfraInput['pub_latency'] = temp.network.public_networks.latency_ms.join(', ');
        this.summaryInfraInput['pvt_dev_cnt'] = 0;
        this.summaryInfraInput['pvt_dev'] = {};
        this.summaryInfraInput['pub_dev'] = {};
        this.summaryInfraInput['dev_cnt'] = 1;
        for (var i in temp1) {
            this.summaryInfraInput['pvt_dev'][i] = 0;
            this.summaryInfraInput['pub_dev'][i] = 0;
            this.summaryInfraInput['dev_cnt'] += 1;
        }
        for (var i in temp['private_networks']) {
            this.summaryInfraInput['pvt_dev_cnt'] += +temp['private_networks'][i]['number_devices'] + 1;
            this.summaryInfraInput['pvt_dev'][temp['private_networks'][i]['device_type']] += +temp['private_networks'][i]['number_devices'] + 1;
        }
        this.summaryInfraInput['pub_dev_cnt'] = 0;
        for (var i in temp['public_networks']) {
            for (var _i = 0, _a = temp['public_networks'][i]; _i < _a.length; _i++) {
                var j = _a[_i];
                this.summaryInfraInput['pub_dev_cnt'] += +j['number_devices'];
                this.summaryInfraInput['pub_dev'][j['device_type']] += +j['number_devices'];
            }
        }
    };
    SetupDataService.prototype.getSummaryInfraOutput = function () {
        var temp = JSON.parse(this.files['infra_config.json']);
        var temp1 = JSON.parse(this.files['infra_gen.json']);
        var temp2 = JSON.parse(this.files['device_types.json']);
        this.summaryInfraOutput['pvt'] = temp['private_networks'];
        this.summaryInfraOutput['pub'] = temp['public_networks'];
        this.summaryInfraOutput['pvt_dev'] = {};
        this.summaryInfraOutput['pub_dev'] = {};
        for (var i in temp1['private_networks']) {
            this.summaryInfraOutput['pvt_dev'][i] = {};
            for (var j in temp2) {
                if (j === temp1['private_networks'][i]['device_type'])
                    this.summaryInfraOutput['pvt_dev'][i][j] = +temp1['private_networks'][i]['number_devices'] + 1;
                else
                    this.summaryInfraOutput['pvt_dev'][i][j] = 0;
            }
        }
        for (var i in temp1['public_networks']) {
            this.summaryInfraOutput['pub_dev'][i] = {};
            for (var k in temp2) {
                this.summaryInfraOutput['pub_dev'][i][k] = 0;
            }
            for (var _i = 0, _a = temp1['public_networks'][i]; _i < _a.length; _i++) {
                var j = _a[_i];
                this.summaryInfraOutput['pub_dev'][i][j['device_type']] = +j['number_devices'];
            }
        }
    };
    SetupDataService.prototype.getInfraInput = function () {
        var _this = this;
        this.http.get(this.url + "infra_gen_input").subscribe(function (res) {
            _this.files['infra_gen.json'] = res['infra_gen.json'];
            _this.files['device_types.json'] = res['device_types.json'];
            _this.inputFileDD['infra'] = ['infra_gen.json'];
            _this.inputInfraFile = _this.inputFileDD['infra'][0];
            _this.getSummaryInfraInput();
        });
    };
    SetupDataService.prototype.getInfraOutput = function () {
        var _this = this;
        this.http.get(this.url + "infra_gen_output").subscribe(function (res) {
            _this.files['infra_config.json'] = res['data'];
            _this.outputFileDD['infra'] = ['infra_config.json'];
            _this.outputInfraFile = _this.outputFileDD['infra'][0];
            _this.getSummaryInfraOutput();
        });
    };
    // Partition
    SetupDataService.prototype.getSummaryPartitionInput = function () {
        this.summaryPartitionInput['vmc'] = JSON.parse(this.files['vm_config.json']);
        this.summaryPartitionInput['vmt'] = JSON.parse(this.files['vm_types.json']);
        this.summaryPartitionInput['dvt'] = JSON.parse(this.files['device_types.json']);
        this.summaryPartitionInput['vm_count'] = Object.keys(this.summaryPartitionInput['vmc']['container_VM']).length;
        this.summaryPartitionInput['used'] = {};
        for (var i in this.summaryPartitionInput['vmt']) {
            this.summaryPartitionInput['used'][i] = 0;
        }
        for (var i in this.summaryPartitionInput['vmc']['container_VM']) {
            this.summaryPartitionInput['used'][this.summaryPartitionInput['vmc']['container_VM'][i]['vm_type']] = 1;
        }
        console.log(this.summaryPartitionInput['used']);
    };
    SetupDataService.prototype.getSummaryPartitionOutput = function () {
        var _this = this;
        var temp = JSON.parse(this.files['metis_partitions.json']);
        var i = 0;
        this.summaryPartitionOutput['cnt'] = {};
        Object.entries(this.summaryPartitionInput['vmc']['container_VM']).forEach(function (_a) {
            var key = _a[0], value = _a[1];
            _this.summaryPartitionOutput['cnt'][i.toString()] = { 'name': key, 'cnt': 0 };
            i++;
        });
        for (var j in temp) {
            this.summaryPartitionOutput['cnt'][temp[j]]['cnt']++;
        }
    };
    SetupDataService.prototype.getPartitionPlots = function () {
        var _this = this;
        this.http.get(this.url + "partition_plot_coremark", { responseType: 'blob' }).subscribe(function (res) {
            _this.createImageFromBlob(res, 'partition_coremark');
            _this.http.get(_this.url + "partition_plot_disk", { responseType: 'blob' }).subscribe(function (res) {
                _this.createImageFromBlob(res, 'partition_disk');
                _this.http.get(_this.url + "partition_plot_memory", { responseType: 'blob' }).subscribe(function (res) {
                    _this.createImageFromBlob(res, 'partition_memory');
                });
            });
        });
    };
    SetupDataService.prototype.getPartitionInput = function () {
        var _this = this;
        this.http.get(this.url + "partition_input").subscribe(function (res) {
            _this.files['vm_config.json'] = res['vm_config.json'];
            _this.files['vm_types.json'] = res['vm_types.json'];
            _this.inputFileDD['partition'] = ['vm_types.json', 'vm_config.json', 'device_types.json'];
            _this.inputPartitionFile = _this.inputFileDD['partition'][0];
            _this.getSummaryPartitionInput();
        });
    };
    SetupDataService.prototype.getPartitionOutput = function () {
        var _this = this;
        this.http.get(this.url + "partition_output").subscribe(function (res) {
            _this.files['metis_partitions.json'] = res['metis_partitions.json'];
            _this.outputFileDD['partition'] = ['metis_partitions.json'];
            _this.outputPartitionFile = _this.outputFileDD['partition'][0];
            _this.getSummaryPartitionOutput();
        });
    };
    // Deployment
    SetupDataService.prototype.getDeploymentInput = function () {
        var _this = this;
        this.http.get(this.url + "deployment_input").subscribe(function (res) {
            _this.files['deployment.json'] = res['deployment.json'];
            _this.files['sensor_types.json'] = res['sensor_types.json'];
            _this.inputFileDD['deployment'] = ['infra_config.json', 'vm_types.json', 'device_types.json', 'vm_config.json',
                'metis_partitions.json', 'deployment.json', 'sensor_types.json'];
            _this.inputDepFile = _this.inputFileDD['deployment'][0];
        });
    };
    SetupDataService.prototype.getDeploymentOutput = function () {
        var _this = this;
        this.http.get(this.url + "deployment_output").subscribe(function (res) {
            _this.files['deployment_output.json'] = res['deployment_output.json'];
            _this.outputFileDD['deployment'] = ['deployment_output.json'];
            _this.outputDepFile = _this.outputFileDD['deployment'][0];
        });
    };
    SetupDataService.prototype.getDeploymentPlots = function () {
        var _this = this;
        this.http.get(this.url + "deployment_plot", { responseType: 'blob' }).subscribe(function (res) {
            _this.createImageFromBlob(res, 'deployment_network');
        });
    };
    SetupDataService.prototype.createImageFromBlob = function (image, name) {
        var _this = this;
        var reader = new FileReader();
        reader.addEventListener("load", function () {
            _this.images[name] = reader.result;
        }, false);
        if (image) {
            reader.readAsDataURL(image);
        }
    };
    // Sanity
    SetupDataService.prototype.getSanityInput = function () {
        this.inputFileDD['sanity'] = ['infra_config.json', 'vm_config.json', 'metis_partitions.json', 'deployment.json',
            'sensor_types.json'];
        this.inputSanFile = this.inputFileDD['sanity'][0];
    };
    SetupDataService.ngInjectableDef = _angular_core__WEBPACK_IMPORTED_MODULE_1__["defineInjectable"]({ factory: function SetupDataService_Factory() { return new SetupDataService(_angular_core__WEBPACK_IMPORTED_MODULE_1__["inject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_0__["HttpClient"])); }, token: SetupDataService, providedIn: "root" });
    return SetupDataService;
}());



/***/ })

}]);
//# sourceMappingURL=layout-layout-module-ngfactory~setup-setup-module-ngfactory.js.map