document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const sidebarOff = document.querySelector(".sidebar-off");
    const personalizarSection = document.getElementById("personalizar-section");
    const DcloseSidebarButton = document.getElementById("d-close-sidebar");
    const WcloseSidebarButton = document.getElementById("w-close-sidebar");
    const closePersonalizarButton = document.getElementById("close-personalizar");
    const personalizarButton = document.getElementById("personalizar");

    function showPersonalizarSection() {
        personalizarSection.classList.remove("hidden");
    }

    function hidePersonalizarSection() {
        personalizarSection.classList.add("hidden");
    }

    function hideSidebar() {
        sidebar.classList.add("hidden");
        sidebarOff.classList.remove("hidden");
    }

    function showSidebar() {
        sidebar.classList.remove("hidden");
        sidebarOff.classList.add("hidden");
    }

    personalizarButton.addEventListener("click", () => {
        if (personalizarSection.classList.contains("hidden")) {
            showPersonalizarSection();
        } else {
            hidePersonalizarSection();
        }
    });

    closePersonalizarButton.addEventListener("click", hidePersonalizarSection);
    DcloseSidebarButton.addEventListener("click", hideSidebar);
    WcloseSidebarButton.addEventListener("click", hideSidebar);
    sidebarOff.addEventListener("click", showSidebar);

    document.addEventListener("click", (event) => {
        if (!personalizarSection.contains(event.target) && !personalizarButton.contains(event.target)) {
            hidePersonalizarSection();
        }
    });
});