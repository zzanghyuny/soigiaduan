/* Danh sách dự án có tab khu vực — đọc mảng DUAN trong du-an-data.js */
(function(){
  function render(box){
    var pageSize=parseInt(box.getAttribute("data-page-size")||"12",10);
    var base=(typeof DUAN!=="undefined"?DUAN.slice():[]).sort(function(a,b){return (b.date||"").localeCompare(a.date||"");});
    if(!base.length){box.innerHTML='<p class="meta">Chưa có bài.</p>';return;}
    var regions=[];base.forEach(function(p){if(p.region&&regions.indexOf(p.region)<0)regions.push(p.region);});
    var active="",shown=0,posts=base;
    var tabs=document.createElement("div");tabs.className="tabs";tabs.setAttribute("role","tablist");
    function mk(label,val){var b=document.createElement("button");b.type="button";b.className="tab"+(val===""?" active":"");b.setAttribute("role","tab");
      var cnt=val===""?base.length:base.filter(function(p){return p.region===val;}).length;b.textContent=label+" ("+cnt+")";
      b.addEventListener("click",function(){active=val;[].forEach.call(tabs.children,function(c){c.classList.remove("active");});b.classList.add("active");reset();});return b;}
    tabs.appendChild(mk("Tất cả",""));regions.forEach(function(r){tabs.appendChild(mk(r,r));});
    box.appendChild(tabs);
    var list=document.createElement("div");list.className="dlist";box.appendChild(list);
    var more=document.createElement("button");more.type="button";more.className="more";more.textContent="Xem thêm";
    function next(){posts.slice(shown,shown+pageSize).forEach(function(p){var a=document.createElement("a");a.className="card";a.href=p.url;
      a.innerHTML='<span class="meta">'+p.dateLabel+' · '+p.tag+'</span><h2 style="margin:6px 0"></h2><span></span>';
      a.querySelector("h2").textContent=p.title;a.lastChild.textContent=p.preview||"";list.appendChild(a);});
      shown=Math.min(posts.length,shown+pageSize);more.style.display=shown<posts.length?"block":"none";}
    function reset(){posts=active?base.filter(function(p){return p.region===active;}):base;list.innerHTML="";shown=0;next();}
    more.addEventListener("click",next);box.appendChild(more);reset();
  }
  document.addEventListener("DOMContentLoaded",function(){[].forEach.call(document.querySelectorAll("[data-feed]"),render);});
})();
