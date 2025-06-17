/**
 * Genesis Engine API Client
 * Centralized API communication for the Genesis Agentic Development Engine
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { config } from './config';
import type { ApiResponse, PaginatedResponse } from '@/types';

class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = config.api.baseUrl;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: config.api.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        // Add request timestamp
        config.metadata = { startTime: new Date() };
        
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        // Log response time in development
        if (config.development.enableDebugMode) {
          const endTime = new Date();
          const startTime = response.config.metadata?.startTime;
          if (startTime) {
            const duration = endTime.getTime() - startTime.getTime();
            console.log(`API Request to ${response.config.url} took ${duration}ms`);
          }
        }
        
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        // Handle 401 errors (unauthorized)
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            await this.refreshToken();
            const token = this.getAuthToken();
            if (token) {
              originalRequest.headers.Authorization = `Bearer ${token}`;
              return this.client(originalRequest);
            }
          } catch (refreshError) {
            this.handleAuthError();
            return Promise.reject(refreshError);
          }
        }

        // Handle network errors with retry
        if (error.code === 'NETWORK_ERROR' && !originalRequest._retryCount) {
          originalRequest._retryCount = 0;
        }

        if (originalRequest._retryCount < config.api.retries) {
          originalRequest._retryCount++;
          const delay = Math.pow(2, originalRequest._retryCount) * 1000;
          await new Promise(resolve => setTimeout(resolve, delay));
          return this.client(originalRequest);
        }

        return Promise.reject(error);
      }
    );
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('genesis_auth_token');
    }
    return null;
  }

  private async refreshToken(): Promise<void> {
    const refreshToken = typeof window !== 'undefined' 
      ? localStorage.getItem('genesis_refresh_token') 
      : null;
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await this.client.post('/auth/refresh', {
      refresh_token: refreshToken,
    });

    const { access_token, refresh_token: newRefreshToken } = response.data;
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('genesis_auth_token', access_token);
      localStorage.setItem('genesis_refresh_token', newRefreshToken);
    }
  }

  private handleAuthError(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('genesis_auth_token');
      localStorage.removeItem('genesis_refresh_token');
      window.location.href = '/login';
    }
  }

  // Generic request methods
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.client.get(url, config);
    return response.data;
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.client.put(url, data, config);
    return response.data;
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.client.patch(url, data, config);
    return response.data;
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.client.delete(url, config);
    return response.data;
  }

  // Specialized API methods
  
  // Authentication
  async login(email: string, password: string) {
    return this.post('/auth/login', { email, password });
  }

  async logout() {
    const response = await this.post('/auth/logout');
    if (typeof window !== 'undefined') {
      localStorage.removeItem('genesis_auth_token');
      localStorage.removeItem('genesis_refresh_token');
    }
    return response;
  }

  async register(userData: { email: string; password: string; name: string }) {
    return this.post('/auth/register', userData);
  }

  // Projects
  async getProjects(params?: { page?: number; limit?: number; search?: string }) {
    return this.get<PaginatedResponse<any>>('/projects', { params });
  }

  async getProject(id: string) {
    return this.get(`/projects/${id}`);
  }

  async createProject(projectData: any) {
    return this.post('/projects', projectData);
  }

  async updateProject(id: string, projectData: any) {
    return this.put(`/projects/${id}`, projectData);
  }

  async deleteProject(id: string) {
    return this.delete(`/projects/${id}`);
  }

  // Agents
  async getAgents(projectId?: string) {
    const url = projectId ? `/projects/${projectId}/agents` : '/agents';
    return this.get(url);
  }

  async getAgent(id: string) {
    return this.get(`/agents/${id}`);
  }

  async createAgent(agentData: any) {
    return this.post('/agents', agentData);
  }

  async updateAgent(id: string, agentData: any) {
    return this.put(`/agents/${id}`, agentData);
  }

  async deleteAgent(id: string) {
    return this.delete(`/agents/${id}`);
  }

  // Tasks
  async getTasks(projectId?: string, params?: { status?: string; assignedAgent?: string }) {
    const url = projectId ? `/projects/${projectId}/tasks` : '/tasks';
    return this.get(url, { params });
  }

  async getTask(id: string) {
    return this.get(`/tasks/${id}`);
  }

  async createTask(taskData: any) {
    return this.post('/tasks', taskData);
  }

  async updateTask(id: string, taskData: any) {
    return this.put(`/tasks/${id}`, taskData);
  }

  async deleteTask(id: string) {
    return this.delete(`/tasks/${id}`);
  }

  async assignTask(taskId: string, agentId: string) {
    return this.post(`/tasks/${taskId}/assign`, { agent_id: agentId });
  }

  // Artifacts
  async getArtifacts(projectId?: string, taskId?: string) {
    let url = '/artifacts';
    if (projectId) url = `/projects/${projectId}/artifacts`;
    if (taskId) url = `/tasks/${taskId}/artifacts`;
    return this.get(url);
  }

  async getArtifact(id: string) {
    return this.get(`/artifacts/${id}`);
  }

  async createArtifact(artifactData: any) {
    return this.post('/artifacts', artifactData);
  }

  async updateArtifact(id: string, artifactData: any) {
    return this.put(`/artifacts/${id}`, artifactData);
  }

  async deleteArtifact(id: string) {
    return this.delete(`/artifacts/${id}`);
  }

  // Code Generation
  async generateCode(prompt: string, context?: any) {
    return this.post('/ai/generate-code', { prompt, context });
  }

  async reviewCode(code: string, language: string) {
    return this.post('/ai/review-code', { code, language });
  }

  async optimizeCode(code: string, language: string) {
    return this.post('/ai/optimize-code', { code, language });
  }

  // System
  async getSystemStatus() {
    return this.get('/system/status');
  }

  async getSystemMetrics() {
    return this.get('/system/metrics');
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
export default apiClient;