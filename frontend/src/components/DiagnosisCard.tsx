import { useState } from "react";

import {
  Box,
  Card,
  CardContent,
  Chip,
 Collapse,
 Divider,
 IconButton,
 Stack,
 Typography,
} from "@mui/material";

import {
  ExpandMore,
  ExpandLess,
 Storage,
 Cloud,
 Dns,
 Folder,
 Computer,
 Lightbulb,
 WarningAmber,
 Inventory2,
 Verified,
} from "@mui/icons-material";

import type { Diagnosis } from "../types/diagnosis";

interface Props {
  diagnosis: Diagnosis;
}

export default function DiagnosisCard({ diagnosis }: Props) {
  const [open, setOpen] = useState(false);

  const severityColor =
    diagnosis.severity === "CRITICAL"
      ? "#d32f2f"
      : diagnosis.severity === "WARNING"
      ? "#ed6c02"
      : "#2e7d32";

  function icon() {
    switch (diagnosis.resource_type) {
      case "Pod":
        return <Storage color="primary" />;

      case "Deployment":
        return <Cloud color="primary" />;

      case "Service":
        return <Dns color="primary" />;

      case "PersistentVolume":
      case "PersistentVolumeClaim":
        return <Folder color="primary" />;

      case "Node":
        return <Computer color="primary" />;

      default:
        return <Storage color="primary" />;
    }
  }

  return (
    <Card
      elevation={6}
      sx={{
        borderRadius: 4,
        mb: 4,
        overflow: "hidden",
        transition: "0.25s",
        "&:hover": {
          transform: "translateY(-4px)",
        },
      }}
    >
      <Box
        sx={{
          height: 8,
          bgcolor: severityColor,
        }}
      />

      <CardContent sx={{ p: 4 }}>
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Stack direction="row" spacing={2} alignItems="center">
            <Box
              sx={{
                width: 58,
                height: 58,
                borderRadius: "50%",
                bgcolor: "action.hover",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              {icon()}
            </Box>

            <Box>
              <Typography variant="h6" fontWeight="bold">
                {diagnosis.resource_name}
              </Typography>

              <Typography color="text.secondary">
                {diagnosis.resource_type}
              </Typography>
            </Box>
          </Stack>

          <Chip
            label={diagnosis.severity}
            color={
              diagnosis.severity === "CRITICAL"
                ? "error"
                : diagnosis.severity === "WARNING"
                ? "warning"
                : "success"
            }
          />
        </Stack>

        <Divider sx={{ my: 3 }} />

        <Stack spacing={2}>

          <Stack direction="row" spacing={1} alignItems="center">
            <Inventory2 color="primary" fontSize="small" />
            <Typography fontWeight="bold">
              Namespace
            </Typography>
          </Stack>

          <Typography color="text.secondary">
            {diagnosis.namespace}
          </Typography>

          <Stack direction="row" spacing={1} alignItems="center">
            <WarningAmber color="warning" fontSize="small" />
            <Typography fontWeight="bold">
              Diagnosis
            </Typography>
          </Stack>

          <Chip
            label={diagnosis.diagnosis}
            color="primary"
            sx={{ width: "fit-content" }}
          />

          <Stack direction="row" spacing={1} alignItems="center">
            <Verified color="success" fontSize="small" />
            <Typography fontWeight="bold">
              Confidence
            </Typography>
          </Stack>

          <Typography color="text.secondary">
            {(diagnosis.confidence * 100).toFixed(0)}%
          </Typography>

        </Stack>

        <Box
          sx={{
            mt: 4,
            p: 3,
            borderRadius: 3,
            bgcolor: "action.hover",
            borderLeft: "6px solid",
            borderColor: "primary.main",
          }}
        >
          <Stack
            direction="row"
            spacing={1}
            alignItems="center"
            mb={1}
          >
            <Lightbulb color="primary" />

            <Typography
              variant="subtitle1"
              fontWeight="bold"
            >
              Recommendation
            </Typography>
          </Stack>

          <Typography
            color="text.primary"
            sx={{
              lineHeight: 1.8,
            }}
          >
            {diagnosis.recommendation}
          </Typography>
        </Box>

        <Box
  sx={{
    mt: 4,
    p: 3,
    borderRadius: 3,
    bgcolor: "action.hover",
    border: "1px solid",
    borderColor: "divider",
  }}
>
  <Stack direction="row" spacing={1} alignItems="center" mb={2}>
    <Typography variant="h6">
      🤖
    </Typography>

    <Box>
      <Typography fontWeight="bold">
        AI Analysis
      </Typography>

      <Typography
        variant="body2"
        color="text.secondary"
      >
        Generated from Kubernetes evidence
      </Typography>
    </Box>
  </Stack>

  <Stack spacing={3}>

    <Box>
      <Typography fontWeight="bold">
        Summary
      </Typography>

      <Typography color="text.secondary">
        {diagnosis.ai.summary}
      </Typography>
    </Box>

    <Box>
      <Typography fontWeight="bold">
        Root Cause
      </Typography>

      <Typography color="text.secondary">
        {diagnosis.ai.root_cause}
      </Typography>
    </Box>

    <Box>
      <Typography fontWeight="bold">
        Impact
      </Typography>

      <Typography color="text.secondary">
        {diagnosis.ai.impact}
      </Typography>
    </Box>

    {diagnosis.ai.verification_steps.length > 0 && (
      <Box>
        <Typography fontWeight="bold" mb={1}>
          Verification Steps
        </Typography>

        <Stack spacing={1}>
          {diagnosis.ai.verification_steps.map((step, index) => (
            <Typography
              key={index}
              color="text.secondary"
            >
              ✓ {step}
            </Typography>
          ))}
        </Stack>
      </Box>
    )}

    {diagnosis.ai.kubectl_commands.length > 0 && (
      <Box>
        <Typography fontWeight="bold" mb={1}>
          Useful kubectl Commands
        </Typography>

        <Stack spacing={1}>
          {diagnosis.ai.kubectl_commands.map((cmd, index) => (
            <Box
              key={index}
              sx={{
                p: 1.5,
                borderRadius: 2,
                bgcolor: "background.default",
                fontFamily: "monospace",
                fontSize: 13,
                overflowX: "auto",
              }}
            >
              {cmd}
            </Box>
          ))}
        </Stack>
      </Box>
    )}

    <Box>
      <Typography fontWeight="bold">
        Prevention
      </Typography>

      <Typography color="text.secondary">
        {diagnosis.ai.prevention}
      </Typography>
    </Box>

  </Stack>
</Box>

<Divider sx={{ my: 3 }} />

<Stack
  direction="row"
  justifyContent="space-between"
  alignItems="center"
>






          <Typography fontWeight="bold">
            Evidence
          </Typography>

          <IconButton onClick={() => setOpen(!open)}>
            {open ? <ExpandLess /> : <ExpandMore />}
          </IconButton>
        </Stack>

        <Collapse in={open}>
          <Stack spacing={1} mt={2}>
            {diagnosis.evidence.map((item, index) => (
              <Typography
                key={index}
                color="text.secondary"
              >
                ✓ {item}
              </Typography>
            ))}
          </Stack>
        </Collapse>

      </CardContent>
    </Card>
  );
}
