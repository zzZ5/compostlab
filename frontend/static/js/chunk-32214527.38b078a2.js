(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-32214527"],{"1fd7":function(t,e,i){"use strict";i("877b")},2419:function(t,e,i){"use strict";i("a41e")},"2f37":function(t,e,i){"use strict";i.r(e);var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"chart-container"},[i("equipment-chart",{attrs:{height:"100%",width:"100%"}})],1)},s=[],a=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"chart-container"},[i("sticky",{attrs:{"z-index":10,"class-name":"sub-navbar draft"}},[i("el-date-picker",{attrs:{type:"datetimerange","picker-options":t.pickerOptions,"range-separator":"to","start-placeholder":"begin time","end-placeholder":"end time","value-format":"yyyy-MM-dd HH:mm:ss"},model:{value:t.interval,callback:function(e){t.interval=e},expression:"interval"}}),i("el-input-number",{attrs:{min:1,max:99999,label:"step"},model:{value:t.query.step,callback:function(e){t.$set(t.query,"step",e)},expression:"query.step"}}),i("el-button",{staticStyle:{"margin-left":"10px"},attrs:{type:"primary",loading:t.loading},on:{click:t.handleDialog}},[t._v(" Custom Option ")]),i("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:t.loading,type:"success"},on:{click:t.submitQuery}},[t._v(" Submit ")])],1),i("div",{staticClass:"chart-main-container"},[i("div",{class:t.className,style:{height:t.height,width:t.width},attrs:{id:t.id}})]),i("el-dialog",{attrs:{title:"Option",visible:t.dialogFormVisible},on:{"update:visible":function(e){t.dialogFormVisible=e}}},[i("div",{staticClass:"header-title",attrs:{slot:"title"},slot:"title"},[i("span",[i("span",{staticStyle:{"font-size":"22px"}},[t._v("Option ")]),i("el-link",{attrs:{type:"primary",href:"https://echarts.apache.org/zh/option.html",target:"_blank"}},[t._v("参考文档")])],1)]),i("json-editor",{ref:"jsonEditor",model:{value:t.tempOption,callback:function(e){t.tempOption=e},expression:"tempOption"}}),i("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{on:{click:function(e){t.dialogFormVisible=!1}}},[t._v(" Cancel ")]),i("el-button",{attrs:{type:"primary"},on:{click:t.handleCustom}},[t._v(" Confirm ")])],1)],1)],1)},r=[],o=(i("159b"),i("313e")),l=i.n(o),d=i("ed08"),c={data:function(){return{$_sidebarElm:null,$_resizeHandler:null}},mounted:function(){this.initListener()},activated:function(){this.$_resizeHandler||this.initListener(),this.resize()},beforeDestroy:function(){this.destroyListener()},deactivated:function(){this.destroyListener()},methods:{$_sidebarResizeHandler:function(t){"width"===t.propertyName&&this.$_resizeHandler()},initListener:function(){var t=this;this.$_resizeHandler=Object(d["b"])((function(){t.resize()}),100),window.addEventListener("resize",this.$_resizeHandler),this.$_sidebarElm=document.getElementsByClassName("sidebar-container")[0],this.$_sidebarElm&&this.$_sidebarElm.addEventListener("transitionend",this.$_sidebarResizeHandler)},destroyListener:function(){window.removeEventListener("resize",this.$_resizeHandler),this.$_resizeHandler=null,this.$_sidebarElm&&this.$_sidebarElm.removeEventListener("transitionend",this.$_sidebarResizeHandler)},resize:function(){var t=this.chart;t&&t.resize()}}},u=i("f564"),h=i("fa7e"),p=i("b804"),m={naem:"EquipmentChart",components:{Sticky:p["a"],JsonEditor:h["a"]},mixins:[c],props:{className:{type:String,default:"chart"},id:{type:String,default:"chart"},width:{type:String,default:"200px"},height:{type:String,default:"200px"}},data:function(){return{chart:null,series:[],option:{legend:{},title:{text:""},toolbox:{feature:{dataZoom:{yAxisIndex:"none"},restore:{},saveAsImage:{},dataView:{}}},tooltip:{trigger:"axis",axisPointer:{animation:!1},formatter:function(t){var e=t[0].data[0]+"</br>";for(var i in t)e+=t[i].marker+t[i].seriesName+": "+t[i].data[1]+t[i].data[2]+"</br>";return e}},grid:{show:!0,containLabel:!0},xAxis:{type:"time",boundaryGap:!1,splitLine:{show:!1}},yAxis:{type:"value",splitLine:{show:!0}},dataZoom:[{type:"inside",realtime:!0,start:0,end:100},{start:0,end:100}]},tempOption:{},pickerOptions:{shortcuts:[{text:"last week",onClick:function(t){var e=new Date,i=new Date;i.setTime(i.getTime()-6048e5),t.$emit("pick",[i,e])}},{text:"last month",onClick:function(t){var e=new Date,i=new Date;i.setTime(i.getTime()-2592e6),t.$emit("pick",[i,e])}},{text:"last three month",onClick:function(t){var e=new Date,i=new Date;i.setTime(i.getTime()-7776e6),t.$emit("pick",[i,e])}}]},dialogFormVisible:!1,loading:!1,experimentId:"0",equipmentId:"0",interval:[],query:{experiment:"0",step:60,count:void 0,begin_time:void 0,end_time:void 0},tempRoute:{}}},watch:{series:function(t){t!==[]&&this.chart.setOption({series:t})}},mounted:function(){this.initChart(),this.fetchData()},beforeDestroy:function(){this.chart&&(this.chart.dispose(),this.chart=null)},created:function(){this.experimentId=this.$route.query&&this.$route.query.experimentId,this.equipmentId=this.$route.params&&this.$route.params.equipmentId,this.query.experiment=this.experimentId,this.tempRoute=Object.assign({},this.$route),this.setTagsViewTitle(),this.setPageTitle(),this.tempOption=this.option},methods:{fetchData:function(){var t=this;this.chart.showLoading(),Object(u["b"])(this.equipmentId,this.query).then((function(e){var i=[{},{type:"custom",name:"error",itemStyle:{normal:{borderWidth:1.5}},renderItem:t.renderItem,encode:{x:0,y:[1,2]},data:[],z:100}],n=e.data;t.interval=[n.begin_time,n.end_time];var s={name:n.abbreviation,type:"line",smooth:!0,showSymbol:!1,data:[]};n.data.forEach((function(t){s.data.push([t[0],t[1],n.unit])})),i[0]=s,i[1].data=n.data,t.series=i,t.chart.hideLoading()}))},initChart:function(){this.chart=l.a.init(document.getElementById(this.id)),this.chart.setOption(this.option)},submitQuery:function(){this.loading=!0,this.query.begin_time=this.interval[0].toLocaleString(),this.query.end_time=this.interval[1].toLocaleString(),this.fetchData(),this.loading=!1},handleDialog:function(){this.dialogFormVisible=!0},handleCustom:function(){this.option=JSON.parse(this.tempOption),this.chart.setOption(this.option),this.dialogFormVisible=!1},setTagsViewTitle:function(){var t="Equipment Chart",e=Object.assign({},this.tempRoute,{title:"".concat(t," - ").concat(this.equipmentId)});this.$store.dispatch("tagsView/updateVisitedView",e)},setPageTitle:function(){var t="Equipment Chart";document.title="".concat(t," - ").concat(this.equipmentId)},renderItem:function(t,e){var i=e.value(0),n=e.coord([i,e.value(2)]),s=e.coord([i,e.value(3)]),a=.1*e.size([1,0])[0],r=e.style({stroke:e.visual("color"),fill:null});return{type:"group",children:[{type:"line",transition:["shape"],shape:{x1:n[0]-a,y1:n[1],x2:n[0]+a,y2:n[1]},style:r},{type:"line",transition:["shape"],shape:{x1:n[0],y1:n[1],x2:s[0],y2:s[1]},style:r},{type:"line",transition:["shape"],shape:{x1:s[0]-a,y1:s[1],x2:s[0]+a,y2:s[1]},style:r}]}}}},f=m,v=(i("2419"),i("2877")),y=Object(v["a"])(f,a,r,!1,null,"ff81d0c2",null),g=y.exports,b={name:"ChartEquipment",components:{EquipmentChart:g}},x=b,w=(i("d1ed"),Object(v["a"])(x,n,s,!1,null,"8142ce16",null));e["default"]=w.exports},"877b":function(t,e,i){},a41e:function(t,e,i){},b804:function(t,e,i){"use strict";var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{style:{height:t.height+"px",zIndex:t.zIndex}},[i("div",{class:t.className,style:{top:t.isSticky?t.stickyTop+"px":"",zIndex:t.zIndex,position:t.position,width:t.width,height:t.height+"px"}},[t._t("default",[i("div",[t._v("sticky")])])],2)])},s=[],a=(i("a9e3"),{name:"Sticky",props:{stickyTop:{type:Number,default:0},zIndex:{type:Number,default:1},className:{type:String,default:""}},data:function(){return{active:!1,position:"",width:void 0,height:void 0,isSticky:!1}},mounted:function(){this.height=this.$el.getBoundingClientRect().height,window.addEventListener("scroll",this.handleScroll),window.addEventListener("resize",this.handleResize)},activated:function(){this.handleScroll()},destroyed:function(){window.removeEventListener("scroll",this.handleScroll),window.removeEventListener("resize",this.handleResize)},methods:{sticky:function(){this.active||(this.position="fixed",this.active=!0,this.width=this.width+"px",this.isSticky=!0)},handleReset:function(){this.active&&this.reset()},reset:function(){this.position="",this.width="auto",this.active=!1,this.isSticky=!1},handleScroll:function(){var t=this.$el.getBoundingClientRect().width;this.width=t||"auto";var e=this.$el.getBoundingClientRect().top;e<this.stickyTop?this.sticky():this.handleReset()},handleResize:function(){this.isSticky&&(this.width=this.$el.getBoundingClientRect().width+"px")}}}),r=a,o=i("2877"),l=Object(o["a"])(r,n,s,!1,null,null,null);e["a"]=l.exports},d1ed:function(t,e,i){"use strict";i("f3fa")},f3fa:function(t,e,i){},f564:function(t,e,i){"use strict";i.d(e,"d",(function(){return s})),i.d(e,"c",(function(){return a})),i.d(e,"a",(function(){return r})),i.d(e,"f",(function(){return o})),i.d(e,"e",(function(){return l})),i.d(e,"b",(function(){return d}));var n=i("b775");function s(t){return Object(n["a"])({url:"/equipment/list/",method:"get",params:t})}function a(t){return Object(n["a"])({url:"/equipment/"+t+"/detail/",method:"get"})}function r(t){return Object(n["a"])({url:"/equipment/create/",method:"post",data:t})}function o(t,e){return Object(n["a"])({url:"/equipment/"+t+"/update/",method:"put",data:e})}function l(t,e){return Object(n["a"])({url:"/equipment/"+t+"/cmd/",method:"post",data:e})}function d(t,e){return Object(n["a"])({url:"/equipment/"+t+"/data/",method:"get",params:e})}},fa7e:function(t,e,i){"use strict";var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"json-editor"},[i("textarea",{ref:"textarea"})])},s=[],a=i("56b3"),r=i.n(a);i("0dd0"),i("a7be"),i("acdf"),i("f9d4"),i("8822"),i("d2de");i("ae67");var o={name:"JsonEditor",props:["value"],data:function(){return{jsonEditor:!1}},watch:{value:function(t){var e=this.jsonEditor.getValue();t!==e&&this.jsonEditor.setValue(JSON.stringify(this.value,null,2))}},mounted:function(){var t=this;this.jsonEditor=r.a.fromTextArea(this.$refs.textarea,{lineNumbers:!0,mode:"application/json",gutters:["CodeMirror-lint-markers"],theme:"rubyblue",lint:!0}),this.jsonEditor.setValue(JSON.stringify(this.value,null,2)),this.jsonEditor.on("change",(function(e){t.$emit("changed",e.getValue()),t.$emit("input",e.getValue())}))},methods:{getValue:function(){return this.jsonEditor.getValue()}}},l=o,d=(i("1fd7"),i("2877")),c=Object(d["a"])(l,n,s,!1,null,"1958ddac",null);e["a"]=c.exports}}]);