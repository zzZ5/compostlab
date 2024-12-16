(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-8289565c"],{1941:function(e,t,a){"use strict";var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"createEquipment-container"},[a("sticky",{attrs:{"z-index":10,"class-name":"sub-navbar draft"}},[a("el-button",{staticStyle:{"margin-left":"10px"},on:{click:e.editForm}},[e._v(" "+e._s(e.status)+" ")]),a("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:e.loading,type:"success"},on:{click:e.submitForm}},[e._v(" Submit ")])],1),a("el-form",{ref:"postForm",staticClass:"form-container",attrs:{disabled:e.isDisabled,model:e.postForm,rules:e.rules}},[a("div",{staticClass:"createEquipment-main-container"},[a("el-row",[a("el-col",{attrs:{span:24}},[a("el-row",[a("el-col",{attrs:{span:12}},[a("el-form-item",{staticStyle:{"margin-bottom":"40px","margin-right":"40px"},attrs:{prop:"name"}},[a("MDinput",{attrs:{disabled:e.isDisabled,maxlength:100,name:"name",required:""},model:{value:e.postForm.name,callback:function(t){e.$set(e.postForm,"name",t)},expression:"postForm.name"}},[e._v(" Name ")])],1)],1),a("el-col",{attrs:{span:12}},[a("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{prop:"abbreviation"}},[a("MDinput",{attrs:{disabled:e.isDisabled,maxlength:100,name:"abbreviation",required:""},model:{value:e.postForm.abbreviation,callback:function(t){e.$set(e.postForm,"abbreviation",t)},expression:"postForm.abbreviation"}},[e._v(" Abbreviation ")])],1)],1)],1),a("div",{staticClass:"postInfo-container"},[a("el-row",[a("el-col",{attrs:{span:8}},[a("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"60px",label:"Type:"}},[a("el-select",{model:{value:e.postForm.type,callback:function(t){e.$set(e.postForm,"type",t)},expression:"postForm.type"}},e._l(e.typeOptions,(function(e,t){return a("el-option",{key:e+t,attrs:{label:e,value:e}})})),1)],1)],1),a("el-col",{attrs:{span:10}},[e.postForm.created_time?a("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"120px",label:"Created Time:"}},[e._v(" "+e._s(e.postForm.created_time)+" ")]):e._e()],1)],1)],1)],1)],1),a("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{"label-width":"70px",label:"Descript:"}},[a("el-input",{staticClass:"article-textarea",attrs:{rows:1,type:"textarea",autosize:"",placeholder:"Please enter the content"},model:{value:e.postForm.descript,callback:function(t){e.$set(e.postForm,"descript",t)},expression:"postForm.descript"}}),a("span",{directives:[{name:"show",rawName:"v-show",value:e.contentShortLength,expression:"contentShortLength"}],staticClass:"word-counter"},[e._v(e._s(e.contentShortLength)+"words")])],1),a("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{"label-width":"70px",label:"Sensor:","label-position":"top"}},[a("el-transfer",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],staticStyle:{"text-align":"left",display:"inline-block"},attrs:{props:{key:"id",label:"name"},titles:["Available","Selected"],data:e.sensorList},on:{change:e.transferChange},model:{value:e.postForm.sensor,callback:function(t){e.$set(e.postForm,"sensor",t)},expression:"postForm.sensor"}},[a("el-pagination",{directives:[{name:"show",rawName:"v-show",value:e.pagination.total_size>0,expression:"pagination.total_size > 0"}],attrs:{slot:"left-footer",total:e.pagination.total_size,"current-page":e.listQuery.page,"page-size":e.listQuery.size,small:"",layout:"prev, pager, next",align:"right"},on:{"update:currentPage":function(t){return e.$set(e.listQuery,"page",t)},"update:current-page":function(t){return e.$set(e.listQuery,"page",t)},"update:pageSize":function(t){return e.$set(e.listQuery,"size",t)},"update:page-size":function(t){return e.$set(e.listQuery,"size",t)},"current-change":e.getSensorList},slot:"left-footer"})],1)],1)],1)])],1)},n=[],s=a("b85c"),r=a("2909"),o=(a("99af"),a("4de4"),a("caad"),a("4ec9"),a("d3b7"),a("2532"),a("3ca3"),a("0643"),a("2382"),a("ddb0"),a("f564")),l=a("669c"),u=a("1aba"),c=a("b804"),d={id:void 0,name:"",abbreviation:"",type:"",descript:"",sensor:[],created_time:void 0},p={name:"EquipmentEdit",components:{Sticky:c["a"],MDinput:u["a"]},props:{isEdit:{type:Boolean,default:!1}},data:function(){var e=this,t=function(t,a,i){""===a?(e.$message({message:t.field+"为必填项",type:"error"}),i(new Error(t.field+"为必填项"))):i()};return{isDisabled:!0,status:"View",postForm:Object.assign({},d),sensorList:[],selectedSensor:[],loading:!1,typeOptions:["RE"],rules:{name:[{validator:t}],abbreviation:[{validator:t}],type:[{validator:t}]},pagination:{total_size:0},listQuery:{page:1,size:20},listLoading:!1,tempRoute:{}}},computed:{contentShortLength:function(){return this.postForm.descript.length}},created:function(){if(this.isEdit){var e=this.$route.params&&this.$route.params.equipmentId;this.fetchData(e),this.status="Edit"}else this.status="View",this.isDisabled=!1;this.getSensorList(),this.tempRoute=Object.assign({},this.$route)},methods:{unique:function(e){var t=new Map;return e.filter((function(e){return!t.has(e.id)&&t.set(e.id,1)}))},getSensorList:function(){var e=this;this.listLoading=!0,Object(l["c"])(this.listQuery).then((function(t){e.sensorList=t.data.list,e.sensorList=[].concat(Object(r["a"])(e.sensorList),Object(r["a"])(e.selectedSensor)),e.sensorList=e.unique(e.sensorList),e.pagination=t.data.pagination,e.listLoading=!1}))},transferChange:function(e,t,a){this.selectedSensor=this.sensorList.filter((function(t){return e.includes(t.id)}))},fetchData:function(e){var t=this;Object(o["c"])(e).then((function(e){t.postForm=e.data;var a,i=[],n=Object(s["a"])(e.data.sensor);try{for(n.s();!(a=n.n()).done;){var r=a.value;t.selectedSensor.push(r),i.push(r.id)}}catch(o){n.e(o)}finally{n.f()}t.postForm.sensor=i,t.setTagsViewTitle(),t.setPageTitle()})).catch((function(e){console.log(e)}))},setTagsViewTitle:function(){var e="Edit Equipment",t=Object.assign({},this.tempRoute,{title:"".concat(e,"-").concat(this.postForm.id)});this.$store.dispatch("tagsView/updateVisitedView",t)},setPageTitle:function(){var e="Edit Equipment";document.title="".concat(e," - ").concat(this.postForm.id)},editForm:function(){"Edit"===this.status?(this.status="View",this.isDisabled=!1):(this.status="Edit",this.isDisabled=!0)},submitForm:function(){var e=this;console.log(this.postForm),this.$refs.postForm.validate((function(t){if(!t)return console.log("error submit!!"),!1;e.isDisabled=!0,e.loading=!0,e.isEdit?Object(o["f"])(e.postForm.id,e.postForm).then((function(t){e.editForm(),e.$notify({title:"Success",message:"Updated successfully",type:"success",duration:2e3})})):Object(o["a"])(e.postForm).then((function(t){e.editForm(),e.$notify({title:"Success",message:"Created successfully",type:"success",duration:2e3})})),e.loading=!1}))}}},m=p,h=(a("dceb"),a("2877")),f=Object(h["a"])(m,i,n,!1,null,"2a68ef2c",null);t["a"]=f.exports},"1aba":function(e,t,a){"use strict";var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"material-input__component",class:e.computedClasses},[a("div",{class:{iconClass:e.icon}},[e.icon?a("i",{staticClass:"el-input__icon material-input__icon",class:["el-icon-"+e.icon]}):e._e(),"email"===e.type?a("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,required:e.required,type:"email"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"url"===e.type?a("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,required:e.required,type:"url"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"number"===e.type?a("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,step:e.step,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,max:e.max,min:e.min,minlength:e.minlength,maxlength:e.maxlength,required:e.required,type:"number"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"password"===e.type?a("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,max:e.max,min:e.min,required:e.required,type:"password"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"tel"===e.type?a("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,required:e.required,type:"tel"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"text"===e.type?a("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,minlength:e.minlength,maxlength:e.maxlength,required:e.required,type:"text"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),a("span",{staticClass:"material-input-bar"}),a("label",{staticClass:"material-label"},[e._t("default")],2)])])},n=[],s=(a("a9e3"),{name:"MdInput",props:{icon:String,name:String,type:{type:String,default:"text"},value:[String,Number],placeholder:String,readonly:Boolean,disabled:Boolean,min:String,max:String,step:String,minlength:Number,maxlength:Number,required:{type:Boolean,default:!0},autoComplete:{type:String,default:"off"},validateEvent:{type:Boolean,default:!0}},data:function(){return{currentValue:this.value,focus:!1,fillPlaceHolder:null}},computed:{computedClasses:function(){return{"material--active":this.focus,"material--disabled":this.disabled,"material--raised":Boolean(this.focus||this.currentValue)}}},watch:{value:function(e){this.currentValue=e}},methods:{handleModelInput:function(e){var t=e.target.value;this.$emit("input",t),"ElFormItem"===this.$parent.$options.componentName&&this.validateEvent&&this.$parent.$emit("el.form.change",[t]),this.$emit("change",t)},handleMdFocus:function(e){this.focus=!0,this.$emit("focus",e),this.placeholder&&""!==this.placeholder&&(this.fillPlaceHolder=this.placeholder)},handleMdBlur:function(e){this.focus=!1,this.$emit("blur",e),this.fillPlaceHolder=null,"ElFormItem"===this.$parent.$options.componentName&&this.validateEvent&&this.$parent.$emit("el.form.blur",[this.currentValue])}}}),r=s,o=(a("8cb3"),a("2877")),l=Object(o["a"])(r,i,n,!1,null,"9d7baaf6",null);t["a"]=l.exports},"4ec9":function(e,t,a){"use strict";var i=a("6d61"),n=a("6566");e.exports=i("Map",(function(e){return function(){return e(this,arguments.length?arguments[0]:void 0)}}),n)},"669c":function(e,t,a){"use strict";a.d(t,"c",(function(){return n})),a.d(t,"d",(function(){return s})),a.d(t,"a",(function(){return r})),a.d(t,"e",(function(){return o})),a.d(t,"b",(function(){return l}));var i=a("b775");function n(e){return Object(i["a"])({url:"/sensor/list/",method:"get",params:e})}function s(e){return Object(i["a"])({url:"/sensor/"+e+"/detail/",method:"get"})}function r(e){return Object(i["a"])({url:"/sensor/create/",method:"post",data:e})}function o(e,t){return Object(i["a"])({url:"/sensor/"+e+"/update/",method:"put",data:t})}function l(e,t){return Object(i["a"])({url:"/sensor/"+e+"/data/",method:"get",params:t})}},"678f":function(e,t,a){},"8cb3":function(e,t,a){"use strict";a("bef9")},b804:function(e,t,a){"use strict";var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{style:{height:e.height+"px",zIndex:e.zIndex}},[a("div",{class:e.className,style:{top:e.isSticky?e.stickyTop+"px":"",zIndex:e.zIndex,position:e.position,width:e.width,height:e.height+"px"}},[e._t("default",[a("div",[e._v("sticky")])])],2)])},n=[],s=(a("a9e3"),a("2c3e"),{name:"Sticky",props:{stickyTop:{type:Number,default:0},zIndex:{type:Number,default:1},className:{type:String,default:""}},data:function(){return{active:!1,position:"",width:void 0,height:void 0,isSticky:!1}},mounted:function(){this.height=this.$el.getBoundingClientRect().height,window.addEventListener("scroll",this.handleScroll),window.addEventListener("resize",this.handleResize)},activated:function(){this.handleScroll()},destroyed:function(){window.removeEventListener("scroll",this.handleScroll),window.removeEventListener("resize",this.handleResize)},methods:{sticky:function(){this.active||(this.position="fixed",this.active=!0,this.width=this.width+"px",this.isSticky=!0)},handleReset:function(){this.active&&this.reset()},reset:function(){this.position="",this.width="auto",this.active=!1,this.isSticky=!1},handleScroll:function(){var e=this.$el.getBoundingClientRect().width;this.width=e||"auto";var t=this.$el.getBoundingClientRect().top;t<this.stickyTop?this.sticky():this.handleReset()},handleResize:function(){this.isSticky&&(this.width=this.$el.getBoundingClientRect().width+"px")}}}),r=s,o=a("2877"),l=Object(o["a"])(r,i,n,!1,null,null,null);t["a"]=l.exports},bef9:function(e,t,a){},dceb:function(e,t,a){"use strict";a("678f")},f564:function(e,t,a){"use strict";a.d(t,"d",(function(){return n})),a.d(t,"c",(function(){return s})),a.d(t,"a",(function(){return r})),a.d(t,"f",(function(){return o})),a.d(t,"e",(function(){return l})),a.d(t,"b",(function(){return u}));var i=a("b775");function n(e){return Object(i["a"])({url:"/equipment/list/",method:"get",params:e})}function s(e){return Object(i["a"])({url:"/equipment/"+e+"/detail/",method:"get"})}function r(e){return Object(i["a"])({url:"/equipment/create/",method:"post",data:e})}function o(e,t){return Object(i["a"])({url:"/equipment/"+e+"/update/",method:"put",data:t})}function l(e,t){return Object(i["a"])({url:"/equipment/"+e+"/cmd/",method:"post",data:t})}function u(e,t){return Object(i["a"])({url:"/equipment/"+e+"/data/",method:"get",params:t})}}}]);