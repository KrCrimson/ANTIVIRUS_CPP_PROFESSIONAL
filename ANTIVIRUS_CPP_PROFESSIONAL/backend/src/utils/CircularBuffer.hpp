#pragma once

#include <vector>
#include <atomic>
#include <mutex>

namespace AntivirusCore {

/**
 * @brief Buffer circular thread-safe para eventos del sistema
 */
template<typename T>
class CircularBuffer {
public:
    explicit CircularBuffer(size_t capacity) 
        : buffer_(capacity), capacity_(capacity), head_(0), tail_(0), size_(0) {}
    
    bool push(const T& item) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (size_ >= capacity_) {
            // Sobrescribir el elemento más antiguo
            tail_ = (tail_ + 1) % capacity_;
        } else {
            size_++;
        }
        
        buffer_[head_] = item;
        head_ = (head_ + 1) % capacity_;
        
        return true;
    }
    
    bool pop(T& item) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (size_ == 0) {
            return false;
        }
        
        item = buffer_[tail_];
        tail_ = (tail_ + 1) % capacity_;
        size_--;
        
        return true;
    }
    
    size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return size_;
    }
    
    bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return size_ == 0;
    }
    
    bool full() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return size_ >= capacity_;
    }

private:
    std::vector<T> buffer_;
    size_t capacity_;
    size_t head_;
    size_t tail_;
    size_t size_;
    mutable std::mutex mutex_;
};

} // namespace AntivirusCore