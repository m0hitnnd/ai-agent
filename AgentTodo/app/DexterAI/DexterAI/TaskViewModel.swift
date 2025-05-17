import SwiftUI

struct Task: Identifiable, Codable {
    let id: Int
    let task: String
    var time: Int?
}

class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = []
    @Published var newTaskText: String = ""
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var editingTask: Task?
    
    private let baseURL = "https://agent-todo-api.onrender.com"
    
    func fetchTasks() {
        guard let url = URL(string: "\(baseURL)/tasks") else { return }
        
        URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                guard let data = data else {
                    self?.errorMessage = "No data received"
                    return
                }
                
                do {
                    let tasks = try JSONDecoder().decode([Task].self, from: data)
                    self?.tasks = tasks.sorted { ($0.time ?? Int.max) < ($1.time ?? Int.max) }
                } catch {
                    self?.errorMessage = "Failed to decode tasks"
                }
            }
        }.resume()
    }
    
    func addTask() {
        guard !newTaskText.isEmpty else { return }
        isLoading = true
        
        guard let url = URL(string: "\(baseURL)/tasks") else { return }
        
        let task = ["task": newTaskText]
        guard let jsonData = try? JSONSerialization.data(withJSONObject: task) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isLoading = false
                
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                self?.newTaskText = ""
                self?.fetchTasks()
            }
        }.resume()
    }
    
    func deleteTask(_ task: Task) {
        guard let url = URL(string: "\(baseURL)/tasks/\(task.id)") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        URLSession.shared.dataTask(with: request) { [weak self] _, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                if let httpResponse = response as? HTTPURLResponse,
                   httpResponse.statusCode == 200 {
                    self?.tasks.removeAll { $0.id == task.id }
                } else {
                    self?.errorMessage = "Failed to delete task"
                }
            }
        }.resume()
    }
    
    func updateTask(_ task: Task, newTaskText: String) {
        guard let url = URL(string: "\(baseURL)/tasks/\(task.id)") else { return }
        
        let updatedTask = ["task": newTaskText]
        guard let jsonData = try? JSONSerialization.data(withJSONObject: updatedTask) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "PUT"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self?.errorMessage = error.localizedDescription
                    return
                }
                
                guard let data = data else {
                    self?.errorMessage = "No data received"
                    return
                }
                
                do {
                    let updatedTask = try JSONDecoder().decode(Task.self, from: data)
                    if let index = self?.tasks.firstIndex(where: { $0.id == task.id }) {
                        self?.tasks[index] = updatedTask
                    }
                } catch {
                    self?.errorMessage = "Failed to decode updated task"
                }
            }
        }.resume()
    }
}


