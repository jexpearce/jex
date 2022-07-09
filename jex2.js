
let showingrabbit = false;
let showingturtle = false;

let rabbitspeedbox = document.getElementById("rabbitspeedbox");
let turtlespeedbox = document.getElementById("turtlespeedbox");
let turtleheadstartbox = document.getElementById("turtleheadstartbox");

let rabbit = document.getElementById("rabbit");
let button = document.getElementsByClassName("button")[0];
let start = document.getElementsByClassName("start")[0];
let run = document.getElementsByClassName("run")[0];
let reload = document.getElementsByClassName("reload")[0];
let catchup = document.getElementsByClassName("catchup")[0];
let rabbitspeed = document.getElementsByClassName("rabbitspeed")[0];

let turtle = document.getElementById("turtle");
let turtlespeed = document.getElementsByClassName("turtlespeed")[0];
let turtleheadstart = document.getElementsByClassName("turtleheadstart")[0];

let rabbitspeedtext = document.getElementsByClassName("rabbitspeedtext")[0];
let turtlespeedtext = document.getElementsByClassName("turtlespeedtext")[0];
let turtleheadstarttext = document.getElementsByClassName("turtleheadstarttext")[0];


let done1 = document.getElementsByClassName("done1")[0];
let done2 = document.getElementsByClassName("done2")[0];
let nextanimal = document.getElementsByClassName("nextanimal")[0];

let solution = document.getElementsByClassName("solution")[0];

rabbit.onclick = showrabbit;
turtle.onclick = showturtle;
done1.onclick = hiderabbit;
done2.onclick = hideturtle;
run.onclick = go;
reload.onclick = restart;

let clicked = 0;

function showrabbit(){
  
if(showingturtle == true){
  return;
}
showingrabbit = true;
button.style = "display:none";
start.style = "display:none";

rabbitspeed.style = "display:block";
rabbitspeedtext.style = "display:block";
done1.style = "display: block";
nextanimal.style = "display: none";

}
function hiderabbit(){
  showingrabbit = false;
/*let harespeed = rabbitspeedbox.value;*/
  

  rabbitspeed.style = "display:none";
  rabbitspeedtext.style = "display:none";
  done1.style = "display: none";
  nextanimal.style = "display: block";

  clicked = clicked + 1;
  if(clicked >= 2){
  nextanimal.style = "display: none";
  run.style = "display: block";
  }
}

function showturtle(){

  if(showingrabbit == true){
    return;
  }
  showingturtle = true;
  nextanimal.style = "display: none";

  button.style = "display:none";
  start.style = "display:none";
  
  turtlespeed.style = "display:block";
  turtleheadstart.style = "display:block";
  turtlespeedtext.style = "display:block";
  turtleheadstarttext.style = "display:block";
  done2.style = "display: block";

  
  }

  function hideturtle(){
    showingturtle = false;
    /*let tortoisespeed = turtlespeedtext.value;
    let tortoiseheadstart = turtleheadstarttext.value;*/
    
  turtlespeed.style = "display:none";
  turtleheadstart.style = "display:none";
  turtlespeedtext.style = "display:none";
  turtleheadstarttext.style = "display:none";
  done2.style = "display: none";
  nextanimal.style = "display: block";

  clicked = clicked + 1;
  if(clicked >= 2){
  nextanimal.style = "display: hide";
  run.style = "display: block";
  }
  
  
  }

 



//turtlespeedbox.value
//rabbitspeedbox.value
//turtleheadstartbox.value

function go(){
 race(turtlespeedbox.value, rabbitspeedbox.value , turtleheadstartbox.value)
}



function race(v100, v200, g00) {

  solution.style = "display: block";

  if (v100.length < 1 ) { 
    solution.innerHTML = "You forgot to put in the tortoise speed.";
    reload.style = "display: block";
    run.style = "display: none";
    return;
  }
  if (v200.length < 1 ) { 
    solution.innerHTML = "You forgot to put in the hare speed.";
    reload.style = "display: block";
    run.style = "display: none";
    return;
  }
  if (g00.length < 1 ) { 
    solution.innerHTML = "You forgot to put in the tortoise headstart.";
    reload.style = "display: block";
    run.style = "display: none";
    return;
  }

  let v10 = v100.replace(/\D/g, '');
  let v20 = v200.replace(/\D/g, '');
  let g0 = g00.replace(/\D/g, '');

  let v1 = parseInt(v10, 10);
  let v2 = parseInt(v20, 10);
  let g = parseInt(g0, 10);

  

  if (v2 < v1) { 
    solution.innerHTML = "Oh No! The hare cannot catch the tortoise! Try again with a greater hare speed.";
    reload.style = "display: block";
    run.style = "display: none";
    return;
  }
  
  var seconds = Math.floor(g / (v2 - v1) * 3600);
  var h = Math.floor(seconds / 3600);
  var m = Math.floor((seconds - h * 3600) / 60);
  var s = seconds - h * 3600 - m * 60;

  if (h > 5) { 
    solution.innerHTML = " It will take the hare " + h + " hours, and " + m + " minutes to catch up the tortoise. That's a lot of running!";
    reload.style = "display: block";
    run.style = "display: none";
    return;
  }
  
  run.style = "display: none";
  
  solution.innerHTML = " It will take the hare " + h + " hours, " + m + " minutes, and " + s + " seconds to catch up the tortoise.";
  reload.style = "display: block";
}

function restart(){
  window.location.reload();
}
    
  