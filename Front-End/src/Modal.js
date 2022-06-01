import * as React from "react";
import { useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import TextField from "@mui/material/TextField";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function BasicModal({ hanldeGenerate, modalOpen }) {
  const [info, setInfo] = useState({});
  const [open, setOpen] = React.useState(false);
  React.useEffect(() => {
    setOpen(false);
  }, [modalOpen]);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleOnClick = () => {
    hanldeGenerate(info);
  };

  return (
    <div>
      <Button variant="contained" color="primary" onClick={handleOpen}>
        Generate
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      ></Modal>
    </div>
  );
}
