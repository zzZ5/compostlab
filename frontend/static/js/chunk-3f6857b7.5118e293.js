(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3f6857b7"],{"1aba":function(e,t,i){"use strict";var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"material-input__component",class:e.computedClasses},[i("div",{class:{iconClass:e.icon}},[e.icon?i("i",{staticClass:"el-input__icon material-input__icon",class:["el-icon-"+e.icon]}):e._e(),"email"===e.type?i("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,required:e.required,type:"email"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"url"===e.type?i("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,required:e.required,type:"url"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"number"===e.type?i("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,step:e.step,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,max:e.max,min:e.min,minlength:e.minlength,maxlength:e.maxlength,required:e.required,type:"number"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"password"===e.type?i("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,max:e.max,min:e.min,required:e.required,type:"password"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"tel"===e.type?i("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,required:e.required,type:"tel"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),"text"===e.type?i("input",{directives:[{name:"model",rawName:"v-model",value:e.currentValue,expression:"currentValue"}],staticClass:"material-input",attrs:{name:e.name,placeholder:e.fillPlaceHolder,readonly:e.readonly,disabled:e.disabled,autocomplete:e.autoComplete,minlength:e.minlength,maxlength:e.maxlength,required:e.required,type:"text"},domProps:{value:e.currentValue},on:{focus:e.handleMdFocus,blur:e.handleMdBlur,input:[function(t){t.target.composing||(e.currentValue=t.target.value)},e.handleModelInput]}}):e._e(),i("span",{staticClass:"material-input-bar"}),i("label",{staticClass:"material-label"},[e._t("default")],2)])])},n=[],s=(i("a9e3"),{name:"MdInput",props:{icon:String,name:String,type:{type:String,default:"text"},value:[String,Number],placeholder:String,readonly:Boolean,disabled:Boolean,min:String,max:String,step:String,minlength:Number,maxlength:Number,required:{type:Boolean,default:!0},autoComplete:{type:String,default:"off"},validateEvent:{type:Boolean,default:!0}},data:function(){return{currentValue:this.value,focus:!1,fillPlaceHolder:null}},computed:{computedClasses:function(){return{"material--active":this.focus,"material--disabled":this.disabled,"material--raised":Boolean(this.focus||this.currentValue)}}},watch:{value:function(e){this.currentValue=e}},methods:{handleModelInput:function(e){var t=e.target.value;this.$emit("input",t),"ElFormItem"===this.$parent.$options.componentName&&this.validateEvent&&this.$parent.$emit("el.form.change",[t]),this.$emit("change",t)},handleMdFocus:function(e){this.focus=!0,this.$emit("focus",e),this.placeholder&&""!==this.placeholder&&(this.fillPlaceHolder=this.placeholder)},handleMdBlur:function(e){this.focus=!1,this.$emit("blur",e),this.fillPlaceHolder=null,"ElFormItem"===this.$parent.$options.componentName&&this.validateEvent&&this.$parent.$emit("el.form.blur",[this.currentValue])}}}),r=s,l=(i("49b7"),i("2877")),o=Object(l["a"])(r,a,n,!1,null,"9d7baaf6",null);t["a"]=o.exports},"2e06":function(e,t,i){"use strict";i("7618")},"49b7":function(e,t,i){"use strict";i("6312")},"4ec9":function(e,t,i){"use strict";var a=i("6d61"),n=i("6566");e.exports=a("Map",(function(e){return function(){return e(this,arguments.length?arguments[0]:void 0)}}),n)},6312:function(e,t,i){},6739:function(e,t,i){"use strict";var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"createExperiment-container"},[i("sticky",{attrs:{"z-index":10,"class-name":"sub-navbar draft"}},[i("el-button",{staticStyle:{"margin-left":"10px"},on:{click:e.editForm}},[e._v(" "+e._s(e.status)+" ")]),i("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:e.loading.publish,disabled:e.isDisabled,type:"success"},on:{click:e.submitForm}},[e._v(" Submit ")])],1),i("el-form",{ref:"postForm",staticClass:"form-container",attrs:{disabled:e.isDisabled,model:e.postForm,rules:e.rules}},[i("div",{staticClass:"createExperiment-main-container"},[i("el-row",[i("el-col",{attrs:{span:24}},[i("el-row",[i("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{prop:"name"}},[i("MDinput",{attrs:{maxlength:100,name:"name",required:"",disabled:e.isDisabled},model:{value:e.postForm.name,callback:function(t){e.$set(e.postForm,"name",t)},expression:"postForm.name"}},[e._v(" Name ")])],1)],1),i("el-row",[i("el-form-item",{staticStyle:{"margin-bottom":"40px","margin-right":"40px"},attrs:{prop:"site"}},[i("MDinput",{attrs:{maxlength:100,name:"site",required:"",disabled:e.isDisabled},model:{value:e.postForm.site,callback:function(t){e.$set(e.postForm,"site",t)},expression:"postForm.site"}},[e._v(" Site ")])],1)],1),i("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{"label-width":"70px",label:"Descripy:"}},[i("el-input",{staticClass:"article-textarea",attrs:{rows:1,type:"textarea",autosize:"",placeholder:"Please enter the content"},model:{value:e.postForm.descript,callback:function(t){e.$set(e.postForm,"descript",t)},expression:"postForm.descript"}}),i("span",{directives:[{name:"show",rawName:"v-show",value:e.contentShortLength,expression:"contentShortLength"}],staticClass:"word-counter"},[e._v(e._s(e.contentShortLength)+"words")])],1),i("div",{staticClass:"postInfo-container"},[i("el-row",[i("el-col",{attrs:{span:8}},[i("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"100px",label:"Begin time:"}},[i("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"Select date and time"},model:{value:e.postForm.begin_time,callback:function(t){e.$set(e.postForm,"begin_time",t)},expression:"postForm.begin_time"}})],1)],1),i("el-col",{attrs:{span:8}},[i("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"100px",label:"End time:"}},[i("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"Select date and time"},model:{value:e.postForm.end_time,callback:function(t){e.$set(e.postForm,"end_time",t)},expression:"postForm.end_time"}})],1)],1),i("el-col",{attrs:{span:8}},[e.postForm.created_time?i("el-form-item",{staticClass:"postInfo-container-item",attrs:{"label-width":"120px",label:"Created Time:"}},[e._v(" "+e._s(e.postForm.created_time)+" ")]):e._e()],1)],1)],1)],1)],1),i("el-row",{staticStyle:{"margin-top":"40px"}},[i("el-form-item",{staticStyle:{"margin-bottom":"50px"},attrs:{"label-width":"100px",label:"User:","label-position":"top"}},[i("el-transfer",{directives:[{name:"loading",rawName:"v-loading",value:e.loading.userList,expression:"loading.userList"}],staticStyle:{"text-align":"left",display:"inline-block"},attrs:{props:{key:"id",label:"username"},titles:["Available","Selected"],data:e.list.user},on:{change:e.userTransferChange},model:{value:e.postForm.user,callback:function(t){e.$set(e.postForm,"user",t)},expression:"postForm.user"}},[i("el-pagination",{directives:[{name:"show",rawName:"v-show",value:e.pagination.user.total_size>0,expression:"pagination.user.total_size > 0"}],attrs:{slot:"left-footer",total:e.pagination.user.total_size,"current-page":e.listQuery.user.page,"page-size":e.listQuery.user.size,small:"",layout:"prev, pager, next",align:"right"},on:{"update:currentPage":function(t){return e.$set(e.listQuery.user,"page",t)},"update:current-page":function(t){return e.$set(e.listQuery.user,"page",t)},"update:pageSize":function(t){return e.$set(e.listQuery.user,"size",t)},"update:page-size":function(t){return e.$set(e.listQuery.user,"size",t)},"current-change":e.getUserList},slot:"left-footer"})],1)],1)],1),i("el-row",[i("el-form-item",{staticStyle:{"margin-bottom":"40px"},attrs:{"label-width":"100px",label:"Equipment:","label-position":"top"}},[i("el-transfer",{directives:[{name:"loading",rawName:"v-loading",value:e.loading.equipmentList,expression:"loading.equipmentList"}],staticStyle:{"text-align":"left",display:"inline-block"},attrs:{props:{key:"id",label:"name"},titles:["Available","Selected"],data:e.list.equipment,format:{noChecked:"${total}",hasChecked:"${checked}/${total}"}},on:{change:e.equipmentTransferChange},model:{value:e.postForm.equipment,callback:function(t){e.$set(e.postForm,"equipment",t)},expression:"postForm.equipment"}},[i("el-pagination",{directives:[{name:"show",rawName:"v-show",value:e.pagination.equipment.total_size>0,expression:"pagination.equipment.total_size > 0"}],attrs:{slot:"left-footer",total:e.pagination.equipment.total_size,"current-page":e.listQuery.equipment.page,"page-size":e.listQuery.equipment.size,small:"",layout:"prev, pager, next",align:"right"},on:{"update:currentPage":function(t){return e.$set(e.listQuery.equipment,"page",t)},"update:current-page":function(t){return e.$set(e.listQuery.equipment,"page",t)},"update:pageSize":function(t){return e.$set(e.listQuery.equipment,"size",t)},"update:page-size":function(t){return e.$set(e.listQuery.equipment,"size",t)},"current-change":e.getEquipmentList},slot:"left-footer"})],1)],1)],1)],1)])],1)},n=[],s=i("b85c"),r=i("2909"),l=(i("4ec9"),i("d3b7"),i("3ca3"),i("ddb0"),i("4de4"),i("99af"),i("caad"),i("2532"),i("a9e3"),i("c114")),o=i("c24f"),u=i("f564"),c=i("1aba"),d=i("b804"),p={id:void 0,name:"",site:"",descript:"",equipment:[],created_time:void 0,begin_time:"",end_time:"",user:[],owner:"",status:"0"},m={name:"ExperimentEdit",components:{Sticky:d["a"],MDinput:c["a"]},props:{isEdit:{type:Boolean,default:!1}},data:function(){var e=this,t=function(t,i,a){""===i?(e.$message({message:t.field+"为必填项",type:"error"}),a(new Error(t.field+"为必填项"))):a()};return{isDisabled:!0,status:"View",postForm:Object.assign({},p),rules:{name:[{validator:t}],site:[{validator:t}],descript:[{validator:t}],begin_time:[{validator:t}],end_time:[{validator:t}]},tempRoute:{},list:{user:[],equipment:[]},selected:{user:[],equipment:[]},loading:{form:!0,publish:!1,userList:!1,equipmentList:!1},pagination:{user:{total_size:0},equipment:{total_size:0}},listQuery:{user:{page:1,size:20},equipment:{page:1,size:20}}}},computed:{contentShortLength:function(){return this.postForm.descript.length}},created:function(){if(this.isEdit){var e=this.$route.params&&this.$route.params.experimentId;this.status="Edit",this.fetchData(e)}else this.status="View",this.isDisabled=!1;this.getUserList(),this.getEquipmentList(),this.tempRoute=Object.assign({},this.$route)},methods:{unique:function(e){var t=new Map;return e.filter((function(e){return!t.has(e.id)&&t.set(e.id,1)}))},getUserList:function(){var e=this;this.loading.userList=!0,Object(o["a"])(this.listQuery.user).then((function(t){e.list.user=t.data.list,e.list.user=[].concat(Object(r["a"])(e.list.user),Object(r["a"])(e.selected.user)),e.list.user=e.unique(e.list.user),e.pagination.user=t.data.pagination,e.loading.userList=!1}))},getEquipmentList:function(){var e=this;this.loading.EquipmentList=!0,Object(u["d"])(this.listQuery.equipment).then((function(t){e.list.equipment=t.data.list,e.list.equipment=[].concat(Object(r["a"])(e.list.equipment),Object(r["a"])(e.selected.equipment)),e.list.equipment=e.unique(e.list.equipment),e.pagination.equipment=t.data.pagination,e.loading.EquipmentList=!1}))},userTransferChange:function(e,t,i){this.selected.user=this.list.user.filter((function(t){return e.includes(t.id)}))},equipmentTransferChange:function(e,t,i){this.selected.equipment=this.list.equipment.filter((function(t){return e.includes(t.id)}))},fetchData:function(e){var t=this;Object(l["b"])(e).then((function(e){t.postForm=e.data,t.postForm.owner=e.data.owner.id;var i,a=[],n=[],r=Object(s["a"])(e.data.user);try{for(r.s();!(i=r.n()).done;){var l=i.value;t.selected.user.push(l),a.push(l.id)}}catch(d){r.e(d)}finally{r.f()}var o,u=Object(s["a"])(e.data.equipment);try{for(u.s();!(o=u.n()).done;){var c=o.value;t.selected.equipment.push(c),n.push(Number(c.id))}}catch(d){u.e(d)}finally{u.f()}t.postForm.user=a,t.postForm.equipment=n,t.setTagsViewTitle(),t.setPageTitle(),t.loading.form=!1})).catch((function(e){console.log(e)}))},setTagsViewTitle:function(){var e="Edit Experiment",t=Object.assign({},this.tempRoute,{title:"".concat(e,"-").concat(this.postForm.id)});this.$store.dispatch("tagsView/updateVisitedView",t)},setPageTitle:function(){var e="Edit Experiment";document.title="".concat(e," - ").concat(this.postForm.id)},editForm:function(){"Edit"===this.status?(this.status="View",this.isDisabled=!1):(this.status="Edit",this.isDisabled=!0)},submitForm:function(){var e=this;this.$refs.postForm.validate((function(t){if(!t)return console.log("error submit!!"),!1;e.loading.publish=!0,e.isEdit?(console.log(e.postForm.begin_time),console.log(e.postForm.end_time),Object(l["f"])(e.postForm.id,e.postForm).then((function(t){e.editForm(),e.$notify({title:"Success",message:"Updated successfully",type:"success",duration:2e3}),e.loading.publish=!1}))):(e.postForm.owner=e.$store.getters.user_id,Object(l["a"])(e.postForm).then((function(t){e.editForm(),e.$notify({title:"Success",message:"Created successfully",type:"success",duration:2e3}),e.loading.publish=!1})))}))}}},h=m,f=(i("2e06"),i("2877")),g=Object(f["a"])(h,a,n,!1,null,"9d64399a",null);t["a"]=g.exports},7618:function(e,t,i){},b804:function(e,t,i){"use strict";var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{style:{height:e.height+"px",zIndex:e.zIndex}},[i("div",{class:e.className,style:{top:e.isSticky?e.stickyTop+"px":"",zIndex:e.zIndex,position:e.position,width:e.width,height:e.height+"px"}},[e._t("default",[i("div",[e._v("sticky")])])],2)])},n=[],s=(i("a9e3"),{name:"Sticky",props:{stickyTop:{type:Number,default:0},zIndex:{type:Number,default:1},className:{type:String,default:""}},data:function(){return{active:!1,position:"",width:void 0,height:void 0,isSticky:!1}},mounted:function(){this.height=this.$el.getBoundingClientRect().height,window.addEventListener("scroll",this.handleScroll),window.addEventListener("resize",this.handleResize)},activated:function(){this.handleScroll()},destroyed:function(){window.removeEventListener("scroll",this.handleScroll),window.removeEventListener("resize",this.handleResize)},methods:{sticky:function(){this.active||(this.position="fixed",this.active=!0,this.width=this.width+"px",this.isSticky=!0)},handleReset:function(){this.active&&this.reset()},reset:function(){this.position="",this.width="auto",this.active=!1,this.isSticky=!1},handleScroll:function(){var e=this.$el.getBoundingClientRect().width;this.width=e||"auto";var t=this.$el.getBoundingClientRect().top;t<this.stickyTop?this.sticky():this.handleReset()},handleResize:function(){this.isSticky&&(this.width=this.$el.getBoundingClientRect().width+"px")}}}),r=s,l=i("2877"),o=Object(l["a"])(r,a,n,!1,null,null,null);t["a"]=o.exports},c114:function(e,t,i){"use strict";i.d(t,"c",(function(){return n})),i.d(t,"b",(function(){return s})),i.d(t,"a",(function(){return r})),i.d(t,"f",(function(){return l})),i.d(t,"d",(function(){return o})),i.d(t,"e",(function(){return u}));var a=i("b775");function n(e){return Object(a["a"])({url:"/experiment/list/",method:"get",params:e})}function s(e){return Object(a["a"])({url:"/experiment/"+e+"/detail/",method:"get"})}function r(e){return Object(a["a"])({url:"/experiment/create/",method:"post",data:e})}function l(e,t){return Object(a["a"])({url:"/experiment/"+e+"/update/",method:"put",data:t})}function o(e,t){return Object(a["a"])({url:"/experiment/"+e+"/cmd/",method:"post",data:t})}function u(e,t){return Object(a["a"])({url:"/experiment/"+e+"/review/",method:"post",data:t})}},f564:function(e,t,i){"use strict";i.d(t,"d",(function(){return n})),i.d(t,"c",(function(){return s})),i.d(t,"a",(function(){return r})),i.d(t,"f",(function(){return l})),i.d(t,"e",(function(){return o})),i.d(t,"b",(function(){return u}));var a=i("b775");function n(e){return Object(a["a"])({url:"/equipment/list/",method:"get",params:e})}function s(e){return Object(a["a"])({url:"/equipment/"+e+"/detail/",method:"get"})}function r(e){return Object(a["a"])({url:"/equipment/create/",method:"post",data:e})}function l(e,t){return Object(a["a"])({url:"/equipment/"+e+"/update/",method:"put",data:t})}function o(e,t){return Object(a["a"])({url:"/equipment/"+e+"/cmd/",method:"post",data:t})}function u(e,t){return Object(a["a"])({url:"/equipment/"+e+"/data/",method:"get",params:t})}}}]);