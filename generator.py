"""
Module untuk generate ID dengan multi-threading
"""

import random
import threading
import time
from threading import Lock, Event
from pattern_checker import PatternChecker
from storage import Storage

class IDGenerator:
    """Kelas untuk generate ID dengan multi-threading"""
    
    def __init__(self, id_length=11, num_threads=4, storage=None):
        """
        Inisialisasi generator
        
        Args:
            id_length: Panjang ID yang ingin dihasilkan (default 11 digit)
            num_threads: Jumlah thread (default 4)
            storage: Objek Storage untuk menyimpan hasil
        """
        self.id_length = id_length
        self.num_threads = num_threads
        self.storage = storage or Storage()
        self.pattern_checker = PatternChecker()
        
        # Thread control
        self.running = False
        self.paused = False
        self.stop_event = Event()
        self.pause_event = Event()
        self.lock = Lock()
        
        # Statistics
        self.total_generated = 0
        self.rare_ids_count = 0
        self.start_time = None
        self.generated_ids = set()
        self.current_id = ""
        
        # Custom patterns
        self.custom_patterns = []
    
    def generate_random_id(self):
        """Generate ID random dengan panjang tertentu"""
        return ''.join(str(random.randint(0, 9)) for _ in range(self.id_length))
    
    def _worker_thread(self, thread_id):
        """
        Thread worker untuk generate ID
        
        Args:
            thread_id: ID thread
        """
        try:
            while not self.stop_event.is_set():
                # Pause check
                self.pause_event.wait()
                
                # Generate ID
                new_id = self.generate_random_id()
                
                # Update current ID
                with self.lock:
                    self.current_id = new_id
                
                # Check if ID is unique
                with self.lock:
                    if new_id in self.generated_ids:
                        continue
                    self.generated_ids.add(new_id)
                    self.total_generated += 1
                
                # Analyze pattern
                patterns = self.pattern_checker.analyze(
                    new_id, 
                    self.custom_patterns
                )
                
                # Jika ada pola, simpan ke storage
                if patterns:
                    with self.lock:
                        self.storage.add_rare_id(new_id, patterns)
                        self.rare_ids_count += 1
        
        except Exception as e:
            self.storage.add_error(
                f"Thread {thread_id} error: {str(e)}", 
                "thread_error"
            )
    
    def start(self, custom_patterns=None):
        """
        Mulai generator
        
        Args:
            custom_patterns: List pola custom (opsional)
        """
        if self.running:
            raise RuntimeError("Generator sudah berjalan!")
        
        self.running = True
        self.stop_event.clear()
        self.pause_event.set()
        self.custom_patterns = custom_patterns or []
        self.start_time = time.time()
        self.total_generated = 0
        self.rare_ids_count = 0
        self.generated_ids.clear()
        
        # Start worker threads
        self.threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(
                target=self._worker_thread, 
                args=(i,),
                daemon=False
            )
            thread.start()
            self.threads.append(thread)
    
    def stop(self):
        """Stop generator dengan aman"""
        if not self.running:
            return
        
        self.running = False
        self.stop_event.set()
        self.pause_event.set()
        
        # Wait untuk semua thread selesai
        for thread in self.threads:
            thread.join(timeout=5)
        
        # Check jika masih ada thread yang berjalan
        for thread in self.threads:
            if thread.is_alive():
                # Force stop jika timeout
                pass
    
    def pause(self):
        """Pause generator"""
        if self.running:
            self.paused = True
            self.pause_event.clear()
    
    def resume(self):
        """Resume generator"""
        if self.running and self.paused:
            self.paused = False
            self.pause_event.set()
    
    def get_speed(self):
        """
        Dapatkan kecepatan generator (ID per detik)
        
        Returns:
            Float kecepatan ID/detik
        """
        if self.start_time is None:
            return 0
        
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            return 0
        
        return self.total_generated / elapsed
    
    def get_statistics(self):
        """
        Dapatkan statistik generator
        
        Returns:
            Dictionary berisi statistik
        """
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        return {
            'total_generated': self.total_generated,
            'rare_ids_count': self.rare_ids_count,
            'unique_ids': len(self.generated_ids),
            'elapsed_time': elapsed,
            'average_speed': self.get_speed(),
            'current_id': self.current_id,
            'is_running': self.running,
            'is_paused': self.paused,
            'active_threads': len([t for t in self.threads if t.is_alive()])
        }
    
    def set_num_threads(self, num_threads):
        """
        Ubah jumlah thread
        
        Args:
            num_threads: Jumlah thread baru
        """
        if self.running:
            raise RuntimeError("Tidak bisa mengubah thread saat generator berjalan!")
        
        self.num_threads = num_threads
    
    def set_id_length(self, id_length):
        """
        Ubah panjang ID
        
        Args:
            id_length: Panjang ID baru
        """
        if self.running:
            raise RuntimeError("Tidak bisa mengubah panjang ID saat generator berjalan!")
        
        if id_length < 5:
            raise ValueError("Panjang ID minimal 5 digit!")
        if id_length > 20:
            raise ValueError("Panjang ID maksimal 20 digit!")
        
        self.id_length = id_length
    
    def add_custom_pattern(self, pattern):
        """
        Tambah pola custom
        
        Args:
            pattern: String pola (contoh: "1?2?3")
        """
        if len(pattern) != self.id_length:
            raise ValueError(
                f"Panjang pattern harus sama dengan ID length ({self.id_length})"
            )
        
        self.custom_patterns.append(pattern)
    
    def get_current_id(self):
        """Dapatkan ID yang sedang diproses"""
        with self.lock:
            return self.current_id
