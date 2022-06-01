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
      >
        <Box sx={style}>
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flexDirection: "column",
            }}
          >
            <Typography variant="h2" gutterBottom component="div">
              KenKen
            </Typography>
            <Typography
              variant="h5"
              gutterBottom
              component="div"
              style={{ margin: "20px 0" }}
            >
              Choose CSP Algorithm
            </Typography>
            <FormControl>
              <RadioGroup
                aria-labelledby="demo-radio-buttons-group-label"
                defaultValue="female"
                name="radio-buttons-group"
                onChange={(e) =>
                  setInfo({ ...info, algorithm: e.target.value })
                }
              >
                <FormControlLabel
                  value="0"
                  control={<Radio />}
                  label="Backtracking"
                />
                <FormControlLabel
                  value="1"
                  control={<Radio />}
                  label="Backtracking with forward checking"
                />
                <FormControlLabel
                  value="2"
                  control={<Radio />}
                  label="Backtracking with forward checking and arc consistency"
                />
              </RadioGroup>
            </FormControl>
            <Typography
              variant="h5"
              gutterBottom
              component="div"
              style={{ marginTop: "30px" }}
            >
              Choose board size:
            </Typography>
            <TextField
              id="standard-basic"
              variant="standard"
              type="number"
              onChange={(e) => setInfo({ ...info, size: e.target.value })}
            />
            <Button
              variant="contained"
              color="primary"
              style={{ margin: "30px 0" }}
              onClick={handleOnClick}
            >
              Generate Puzzle
            </Button>
          </div>
        </Box>
      </Modal>
    </div>
  );
}
