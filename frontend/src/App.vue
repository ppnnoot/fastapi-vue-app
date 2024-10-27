<template>
  <div style="margin: 0 auto">
    <div style="">
      <div style="height: 60px; width: 100%; background-color: #ccc">
        <RouterLink to="/manageparts">
          <button
            class="nav-button"
            style="
              height: 100%;
              align-content: center;
              border: none; 
              background-color: transparent;
              font-size: 24px;
              font-weight: bold;

            "
          >
            Manage Parts
          </button>
        </RouterLink>
      </div>
    </div>
    <div style="width: 80%; margin: 0 auto">
      <RouterView />
    </div>
  </div>
</template>
