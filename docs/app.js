const toggle=document.querySelector('.menu-toggle');
toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));document.querySelector('.sidebar').classList.toggle('open',open);});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&toggle){toggle.setAttribute('aria-expanded','false');document.querySelector('.sidebar').classList.remove('open');}});

document.querySelectorAll('[data-equipment]').forEach(button=>{
  button.addEventListener('click',()=>{
    document.querySelectorAll('[data-equipment]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
    document.querySelectorAll('.equipment-panel').forEach(panel=>{panel.hidden=panel.id!=='equipment-'+button.dataset.equipment;});
  });
});

const probability=document.querySelector('#probability');
if(probability){
  const steps=document.querySelector('#steps');
  const attempts=document.querySelector('#attempts');
  const update=()=>{
    const p=Number(probability.value)/100, n=Number(steps.value), r=Number(attempts.value);
    const q=1-Math.pow(1-p,r);
    document.querySelector('#probability-label').textContent=p.toFixed(2);
    document.querySelector('#steps-label').textContent=String(n);
    document.querySelector('#base-success').textContent=(100*Math.pow(p,n)).toFixed(1)+'%';
    document.querySelector('#retry-success').textContent=(100*Math.pow(q,n)).toFixed(1)+'%';
    document.querySelector('#max-calls').textContent=String(n*r)+' 次';
  };
  [probability,steps,attempts].forEach(control=>control.addEventListener('input',update));
  update();
}

// Native disclosure elements work without JavaScript; reveal answers in print.
let printOpen=[];
window.addEventListener('beforeprint',()=>{
  printOpen=Array.from(document.querySelectorAll('details')).map(element=>[element,element.open]);
  printOpen.forEach(([element])=>{element.open=true;});
});
window.addEventListener('afterprint',()=>{printOpen.forEach(([element,wasOpen])=>{element.open=wasOpen;});});

function revealPaper(){
  let key; try{key=decodeURIComponent(location.hash.slice(1));}catch{return;}
  const entry=document.getElementById(key);
  if(entry?.classList.contains('paper-entry')){const details=entry.querySelector('details');if(details)details.open=true;}
}
window.addEventListener('hashchange',revealPaper);
revealPaper();
