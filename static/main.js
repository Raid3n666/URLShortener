function copyEvent(id)
{
    var str = document.getElementById(id);
    window.getSelection().selectAllChildren(str);
    document.execCommand("Copy")
    document.createElement('p');
    const par = document.getElementById('copied')
    par.innerHTML = 'COPIED';
    document.body.appendChild(par);
}