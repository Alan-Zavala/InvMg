var sideBarIsOpen = true;

// sideMenu minimizier//
toggleBtn.addEventListener('click', (event) => {
    event.preventDefault();
    
    if(sideBarIsOpen){
        dashboard_sidebar.style.width = '10%';
        dashboard_sidebar.style.transition = '.5s all';
        dashboard_content_container.style.width = '90%';
        dashboard_logo.style.fontSize = '60px';
        userImg.style.width = '40px';
        userImg.style.height = '40px';
        userImg.style.transition = '.5s all'

        menuIcons = document.getElementsByClassName('menuText');
        for(var i=0;i < menuIcons.length;i++){
            menuIcons[i].style.display = 'none';
        }

        document.getElementsByClassName('dashboard_menu_list')[0].style.textAlign = 'center';
        sideBarIsOpen = false;
    } else {
        dashboard_sidebar.style.width = '25%';
        dashboard_content_container.style.width = '75%';
        dashboard_logo.style.fontSize = '60px';
        userImg.style.width = '65px';
        userImg.style.height = '65px';

        menuIcons = document.getElementsByClassName('menuText');
        for(var i=0;i < menuIcons.length;i++){
            menuIcons[i].style.display = 'inline-block';
        }

        document.getElementsByClassName('dashboard_menu_list')[0].style.textAlign = 'left';
        sideBarIsOpen = true;
    }
})

// Submenu show/hide //
document.addEventListener('click', function(e){
    let clickedE1 = e.target;

    if(clickedE1.classList.contains('showHideSubMenu')){
        let subMenu = clickedE1.closest('li').querySelector('.subMenus');
        let mainMenuIcon = clickedE1.closest('li').querySelector('.mainMenuIconArrow');

        // close submenus
        let subMenus = document.querySelectorAll('.subMenus');
        subMenus.forEach((sub) => {
            if(subMenu !== sub) sub.style.display='none';
        });

        showHideSubMenu(subMenu, mainMenuIcon);
    }
});

function showHideSubMenu(subMenu, mainMenuIcon){
    if(subMenu != null){
        if(subMenu.style.display==='block'){
            subMenu.style.display = 'none';
            mainMenuIcon.classList.remove('fa-angle-down');
            mainMenuIcon.classList.add('fa-angle-left');
        } else {
            subMenu.style.display = 'block';
            mainMenuIcon.classList.remove('fa-angle-left');
            mainMenuIcon.classList.add('fa-angle-down');
        }
    }
}

let pathArray = window.location.pathname.split('/');
let curFile = pathArray[pathArray.length - 1];

let curNav = document.querySelector('a[href="./' + curFile + '"]');
curNav.classList.add('subMenuActive');

let mainNav = curNav.closest('li.liMainMenu');
mainNav.style.background = '#f685a1';

let subMenu = curNav.closest('.subMenus');
let mainMenuIcon = mainNav.querySelector('i.mainMenuIconArrow');

showHideSubMenu(subMenu, mainMenuIcon);

console.log(mainNav);