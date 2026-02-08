'use client';

import { useState, useEffect } from 'react';
import { Task } from '@/types';
import TaskList from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';
import DashboardLayout from '@/components/ui/DashboardLayout';
import { apiClient } from '@/services/api-client';
import { betterAuthService } from '@/services/auth-service';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);
  const [currentUser, setCurrentUser] = useState<{ id: string; email: string; name?: string } | null>(null);

  // Get current user ID from BetterAuth
  useEffect(() => {
    const checkAuth = async () => {
      const isAuthenticated = await betterAuthService.isAuthenticated();
      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        router.push('/auth/login');
        return;
      }

      const user = await betterAuthService.getCurrentUser();
      if (user) {
        // Use the user ID from BetterAuth - converting to number since BetterAuth uses string IDs
        setCurrentUserId(parseInt(user.id) || 0);
        setCurrentUser(user);
      }
    };

    checkAuth();
  }, [router]);

  // Fetch tasks when component mounts
  useEffect(() => {
    if (currentUserId) {
      fetchTasks();
    }
  }, [currentUserId]);

  const fetchTasks = async () => {
    if (!currentUserId) return;

    try {
      setLoading(true);
      setError(null);
      const tasksData = await apiClient.getTasks(currentUserId);
      setTasks(tasksData);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  const handleFormSubmit = async (taskData: { title: string; description?: string }) => {
    if (!currentUserId) return;

    try {
      if (editingTask) {
        // Update existing task
        const updatedTask = await apiClient.updateTask(
          currentUserId,
          editingTask.id,
          taskData
        );
        setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
      } else {
        // Create new task
        const newTask = await apiClient.createTask(currentUserId, taskData);
        setTasks([newTask, ...tasks]); // Add to the beginning to show newest first
      }
      setShowForm(false);
      setEditingTask(null);
    } catch (err) {
      console.error('Error saving task:', err);
      setError(err instanceof Error ? err.message : 'Failed to save task');
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleToggleTask = async (task: Task) => {
    if (!currentUserId) return;

    try {
      const toggledTask = await apiClient.toggleTaskCompletion(currentUserId, task.id);
      setTasks(tasks.map(t => t.id === task.id ? toggledTask : t));
    } catch (err) {
      console.error('Error toggling task:', err);
      setError(err instanceof Error ? err.message : 'Failed to toggle task');
    }
  };

  const handleDeleteTask = async (task: Task) => {
    if (!currentUserId) return;

    try {
      await apiClient.deleteTask(currentUserId, task.id);
      setTasks(tasks.filter(t => t.id !== task.id));
    } catch (err) {
      console.error('Error deleting task:', err);
      setError(err instanceof Error ? err.message : 'Failed to delete task');
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  if (!currentUserId) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="flex items-center">
          <p>Redirecting to login</p>
          <div className="ml-2 flex space-x-1">
            <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <DashboardLayout user={currentUser || undefined}>
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="mb-10">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div className="flex-1">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                Task Dashboard
              </h1>
              <p className="text-gray-600 mt-3 text-lg">Manage your tasks efficiently and stay organized</p>

              {/* Stats Card */}
              <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-5 border border-blue-100 shadow-sm">
                  <div className="text-blue-800 text-2xl font-bold">{tasks.length}</div>
                  <div className="text-blue-600 text-sm font-medium">Total Tasks</div>
                </div>
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-5 border border-green-100 shadow-sm">
                  <div className="text-green-800 text-2xl font-bold">{tasks.filter(t => t.completed).length}</div>
                  <div className="text-green-600 text-sm font-medium">Completed</div>
                </div>
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl p-5 border border-orange-100 shadow-sm">
                  <div className="text-orange-800 text-2xl font-bold">{tasks.filter(t => !t.completed).length}</div>
                  <div className="text-orange-600 text-sm font-medium">Pending</div>
                </div>
              </div>
            </div>

            <button
              onClick={handleAddTask}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl flex items-center justify-center space-x-3 min-w-fit transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <span className="text-lg">{showForm && !editingTask ? 'Cancel' : 'Add New Task'}</span>
            </button>
          </div>
        </div>

        {/* Task Form */}
        {showForm && (
          <div className="mb-8 animate-in slide-in-from-top-4 duration-300">
            <div className="bg-white rounded-2xl shadow-lg border border-gray-200/50 p-6">
              <TaskForm
                onSubmit={handleFormSubmit}
                onCancel={handleFormCancel}
                initialData={editingTask ? {
                  title: editingTask.title,
                  description: editingTask.description,
                  completed: editingTask.completed
                } : undefined}
              />
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-8 bg-red-50 border-l-4 border-red-500 p-5 rounded-2xl animate-in slide-in-from-right-4 duration-300 shadow-sm">
            <div className="flex items-start">
              <div className="flex-shrink-0 pt-0.5">
                <svg className="h-6 w-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-semibold text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Task List */}
        <div className="animate-in fade-in-50 duration-500">
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200/50 overflow-hidden">
            <TaskList
              tasks={tasks}
              onToggle={handleToggleTask}
              onDelete={handleDeleteTask}
              onEdit={handleEditTask}
              loading={loading}
            />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}