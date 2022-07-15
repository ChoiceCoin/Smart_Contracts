import { useSelector } from "react-redux";
import { NavLink, Route, Routes } from "react-router-dom";
import navbar from "./statics";
import contract from "./components";

const MainPage = () => {
  const darkTheme = useSelector((state) => state.status.darkTheme);
  return (
    <main
      className={`${
        darkTheme ? "dark_theme big_screen" : "light_theme big_screen"
      }`}
      id="main_main"
    >
      <div
        style={{
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          content: "",
          width: "100%",
          height: "100%",
          opacity: darkTheme ? 0.008 : 0.018,
          position: "fixed",
          pointerEvents: "none",

        }}
        className="contract__background"
      />
      <TopNavigationBar darkTheme={darkTheme} NavLink={NavLink} />
      <Routes>
        {/* <Route path="/schedule" element={<Schedule />} /> */}
        <Route path="/" element={<contract/>}  />
      </Routes>
    </main>
  );
};

export default MainPage;
