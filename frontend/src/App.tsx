import { useMemo, useState } from "react";

import {
  CssBaseline,
  IconButton,
  ThemeProvider,
} from "@mui/material";

import {
  DarkMode,
  LightMode,
} from "@mui/icons-material";

import Dashboard from "./pages/Dashboard";
import Header from "./components/Header";

import {
  darkTheme,
  lightTheme,
} from "./theme";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  const theme = useMemo(
    () => (darkMode ? darkTheme : lightTheme),
    [darkMode]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />

      <Header />

      <IconButton
        onClick={() => setDarkMode(!darkMode)}
        sx={{
          position: "fixed",
          top: 20,
          right: 20,
          bgcolor: "background.paper",
          boxShadow: 3,
          zIndex: 1000,
        }}
      >
        {darkMode ? <LightMode /> : <DarkMode />}
      </IconButton>

      <Dashboard />
    </ThemeProvider>
  );
}
