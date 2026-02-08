import React from 'react';
import { Task } from '@/types';

interface TaskItemProps {
  task: Task;
  onToggle: (task: Task) => void;
  onDelete: (task: Task) => void;
  onEdit: (task: Task) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete, onEdit }) => {
  const handleToggle = () => {
    onToggle(task);
  };

  const handleDelete = () => {
    onDelete(task);
  };

  const handleEdit = () => {
    onEdit(task);
  };

  return (
    <div className={`group relative bg-white rounded-2xl border transition-all duration-300 overflow-hidden hover:shadow-lg ${
      task.completed
        ? 'border-green-200/70 bg-linear-to-r from-green-50/30 to-emerald-50/30'
        : 'border-gray-200/50 hover:border-blue-200/60'
    }`}>
      <div className="p-5">
        <div className="flex items-start space-x-4">
          <div className="flex items-center h-6 mt-0.5">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggle}
              className={`h-5 w-5 rounded-full border-2 transition-all duration-200 cursor-pointer ${
                task.completed
                  ? 'border-green-500 bg-green-500'
                  : 'border-gray-300 hover:border-blue-400 focus:ring-blue-500'
              }`}
            />
          </div>

          <div className="flex-1 min-w-0">
            <h3 className={`text-base font-semibold transition-all duration-200 ${
              task.completed
                ? 'line-through text-gray-500'
                : 'text-gray-800 group-hover:text-gray-900'
            }`}>
              {task.title}
            </h3>

            {task.description && (
              <p className={`mt-2 text-sm ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              } transition-colors duration-200`}>
                {task.description}
              </p>
            )}

            <div className="flex items-center space-x-4 mt-4 text-xs text-gray-500">
              <span className="flex items-center space-x-1.5">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
              </span>

              {task.completed && (
                <span className="flex items-center space-x-1.5 text-green-600 font-medium">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Completed</span>
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-1.5 opacity-0 group-hover:opacity-100 transition-all duration-200">
            <button
              onClick={handleEdit}
              className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              title="Edit task"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>

            <button
              onClick={handleDelete}
              className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
              title="Delete task"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Progress bar for completed tasks */}
      {task.completed && (
        <div className="h-1 bg-linear-to-r from-green-200/50 to-emerald-200/50">
          <div className="h-full bg-linear-to-r from-green-500 to-emerald-500 w-full"></div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;