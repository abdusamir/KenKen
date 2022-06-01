import * as React from "react";
import TextField from "@mui/material/TextField";

const Cell = ({ cell, handleOnChange, id, solve, answer }) => {
  const { bottom, left, right, top, value } = cell;

  return (
    <div>
      <TextField
        style={{
          width: 70,
          marginBottom: "15px",
          paddingTop: value == 0 ? "22px" : "0px",
        }}
      />
    </div>
  );
};

export default Cell;
