function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const pageContent = document.getElementById('page-content-success');
  
    if (sidebar.style.width === '0px' || sidebar.style.width === '') {
      sidebar.style.width = '250px';
      pageContent.style.marginLeft = '250px';
    } else {
      sidebar.style.width = '5px';
      pageContent.style.marginLeft = '0px';
    }
  }
  