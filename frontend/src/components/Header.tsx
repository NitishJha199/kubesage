import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
} from "@mui/material";

export default function Header() {
  return (
    <AppBar
      position="static"
      elevation={1}
      sx={{
        background: "#1565c0",
        borderRadius: 0,
      }}
    >
      <Toolbar
        sx={{
          justifyContent: "space-between",
          py: 1,
        }}
      >
        <Box>
          <Typography
            variant="h4"
            fontWeight="bold"
          >
            🚀 KubeSage
          </Typography>

          <Typography
            variant="subtitle1"
            sx={{ opacity: 0.9 }}
          >
            AI Powered Kubernetes Diagnostics
          </Typography>
        </Box>

        <Box textAlign="right">
          <Typography fontWeight="bold">
            Demo Cluster
          </Typography>

          <Chip
            color="success"
            label="Connected"
            size="small"
            sx={{ mt: 1 }}
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
}
