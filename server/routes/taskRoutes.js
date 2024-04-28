
const express = require("express");
const router = express.Router();
const Task = require("../models/taskModel");

// Get all tasks
router.get("/", async (req, res) => {
  try {
    const tasks = await Task.find();
    res.status(200).json(tasks);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Create a task
router.post("/", async (req, res) => {
  const task = new Task({
    title: req.body.title,
    description: req.body.description,
  });
  try {
    const newTask = await task.save();
    res.status(200).json(newTask);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Update a task
router.patch("/:id", async (req, res) => {
  try {
    const task = await Task.findById(req.params.id);
    if (req.body.title) {
      task.title = req.body.title;
    }
    if (req.body.description) {
      task.description = req.body.description;
    }
    const updatedTask = await task.save();
    res.status(200).json(updatedTask);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Delete a task
router.delete("/:id", async (req, res) => {
  try {
    await Task.findByIdAndDelete(req.params.id);
    res.status(200).json({ message: "Task deleted" });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Remove a task
router.patch("/remove/:id", async (req, res) => {
  try {
    const task = await Task.findById(req.params.id);
    task.removed = !task.removed;
    const removedTask = await task.save();
    res.status(200).json(removedTask);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

module.exports = router;