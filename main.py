#!/usr/bin/env python3
"""
Free Fire ID Generator - Main Application
Generator ID numerik 11 digit dengan multi-threading dan analisis pola
"""

import sys
import os
import time
import json
import threading
from colorama import Fore, Back, Style, init

# Import modul internal
from generator import IDGenerator
from pattern_checker import PatternChecker
from storage import Storage
from display import Display
from account_creator import AccountCreator, APIRateLimiter

# Inisialisasi colorama
init(autoreset=True)

class FFIDGeneratorApp:
    """Aplikasi utama Free Fire ID Generator"""
    
    def __init__(self):
        """Inisialisasi aplikasi"""
        self.storage = Storage()
        self.generator = None
        self.display = Display()
        self.account_creator = None
        self.running = False
        self.lock = threading.Lock()
        
        # Load config
        self.config = self._load_config()
        
        # Default settings
        self.num_threads = self.config.get('default_threads', 4)
        self.id_length = self.config.get('default_id_length', 11)
        self.custom_patterns = []
    
    def _load_config(self):
        """Load konfigurasi dari config.json"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.display.print_warning("config.json tidak ditemukan, menggunakan default config")
            return {
                'default_threads': 4,
                'default_id_length': 11,
                'output_dir': './output',
                'logs_dir': './logs'
            }
        except json.JSONDecodeError:
            self.display.print_error("Gagal membaca config.json")
            return {}
    
    def show_main_menu(self):
        """Tampilkan menu utama"""
        while True:
            os.system('clear' if sys.platform != 'win32' else 'cls')
            self.display.print_header("FREE FIRE ID GENERATOR v1.0")
            self.display.print_menu()
            
            choice = input(f"{Fore.CYAN}Pilih menu [1-6]: {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.start_generator_normal()
            elif choice == '2':
                self.start_generator_custom()
            elif choice == '3':
                self.show_settings_menu()
            elif choice == '4':
                self.show_pattern_info()
            elif choice == '5':
                self.read_results()
            elif choice == '6':
                self.exit_app()
            else:
                self.display.print_error("Pilihan tidak valid!")
                time.sleep(1)
    
    def start_generator_normal(self):
        """Mulai generator mode normal"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
        self.display.print_header("GENERATOR MODE - NORMAL")
        
        # Confirm start
        self.display.print_info(f"Thread: {self.num_threads}, ID Length: {self.id_length}")
        confirm = input(f"\n{Fore.YELLOW}Mulai generator? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if confirm != 'y':
            return
        
        # Duration input
        print(f"\n{Fore.CYAN}Masukkan durasi (detik):{Style.RESET_ALL}")
        try:
            duration = int(input(f"{Fore.YELLOW}Durasi: {Style.RESET_ALL}"))
            if duration <= 0:
                self.display.print_error("Durasi harus lebih dari 0!")
                time.sleep(2)
                return
        except ValueError:
            self.display.print_error("Input tidak valid!")
            time.sleep(2)
            return
        
        # Start generator
        self.generator = IDGenerator(
            id_length=self.id_length,
            num_threads=self.num_threads,
            storage=self.storage
        )
        
        try:
            self.generator.start(custom_patterns=self.custom_patterns)
            self._run_generator_loop(duration)
        except Exception as e:
            self.display.print_error(f"Error: {str(e)}")
            self.storage.add_error(str(e), "generator_error")
        finally:
            self._stop_generator()
    
    def start_generator_custom(self):
        """Mulai generator dengan custom pattern"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
        self.display.print_header("GENERATOR MODE - CUSTOM PATTERN")
        
        self.display.print_info("Input custom pattern menggunakan '?' untuk wildcard")
        self.display.print_info(f"Contoh untuk {self.id_length} digit: 1?2?3???1?3")
        
        patterns = []
        while True:
            pattern = input(f"\n{Fore.YELLOW}Masukkan pattern (atau 'done' untuk mulai): {Style.RESET_ALL}").strip()
            
            if pattern.lower() == 'done':
                if not patterns:
                    self.display.print_error("Minimal 1 pattern harus diinput!")
                    continue
                break
            
            if len(pattern) != self.id_length:
                self.display.print_error(f"Panjang pattern harus {self.id_length} karakter!")
                continue
            
            # Validate pattern
            valid = True
            for char in pattern:
                if char not in '0123456789?':
                    valid = False
                    break
            
            if not valid:
                self.display.print_error("Pattern hanya boleh berisi digit 0-9 dan '?'!")
                continue
            
            patterns.append(pattern)
            self.display.print_success(f"Pattern ditambahkan: {pattern}")
        
        # Duration input
        print(f"\n{Fore.CYAN}Masukkan durasi (detik):{Style.RESET_ALL}")
        try:
            duration = int(input(f"{Fore.YELLOW}Durasi: {Style.RESET_ALL}"))
            if duration <= 0:
                self.display.print_error("Durasi harus lebih dari 0!")
                time.sleep(2)
                return
        except ValueError:
            self.display.print_error("Input tidak valid!")
            time.sleep(2)
            return
        
        # Start generator
        self.generator = IDGenerator(
            id_length=self.id_length,
            num_threads=self.num_threads,
            storage=self.storage
        )
        
        try:
            self.generator.start(custom_patterns=patterns)
            self._run_generator_loop(duration)
        except Exception as e:
            self.display.print_error(f"Error: {str(e)}")
            self.storage.add_error(str(e), "generator_error")
        finally:
            self._stop_generator()
    
    def _run_generator_loop(self, duration):
        """Loop utama generator dengan monitoring"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
        self.display.print_header("GENERATOR RUNNING")
        
        print(f"{Fore.GREEN}Generator sedang berjalan...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Tekan Ctrl+C untuk stop{Style.RESET_ALL}\n")
        
        start_time = time.time()
        refresh_rate = self.config.get('display_refresh_rate', 1)
        last_update = 0
        
        try:
            while time.time() - start_time < duration:
                current_time = time.time() - start_time
                
                if current_time - last_update >= refresh_rate:
                    stats = self.generator.get_statistics()
                    
                    self.display.print_status_bar(
                        stats['current_id'],
                        stats['total_generated'],
                        stats['rare_ids_count'],
                        stats['average_speed'],
                        "Running"
                    )
                    
                    last_update = current_time
                
                time.sleep(0.1)
            
            print()
            self.display.print_success("Durasi selesai!")
        
        except KeyboardInterrupt:
            print()
            self.display.print_warning("Generator dihentikan oleh user")
        
        time.sleep(1)
    
    def _stop_generator(self):
        """Stop generator dengan aman"""
        if self.generator:
            print(f"\n{Fore.YELLOW}Menghentikan generator...{Style.RESET_ALL}")
            self.generator.stop()
            
            # Tampilkan statistik
            stats = self.generator.get_statistics()
            self.display.print_statistics(
                stats['total_generated'],
                stats['rare_ids_count'],
                stats['elapsed_time'],
                stats['active_threads'],
                stats['average_speed']
            )
            
            # Save results
            print(f"\n{Fore.CYAN}Menyimpan hasil...{Style.RESET_ALL}")
            results = self.storage.save_all()
            
            if results['txt']:
                self.display.print_success(f"Hasil TXT disimpan: {results['txt']}")
            if results['json']:
                self.display.print_success(f"Hasil JSON disimpan: {results['json']}")
            if results['log']:
                self.display.print_success(f"Error log disimpan: {results['log']}")
            
            print(f"\n{Fore.YELLOW}Tekan Enter untuk kembali ke menu...{Style.RESET_ALL}")
            input()
    
    def show_settings_menu(self):
        """Tampilkan menu pengaturan"""
        while True:
            os.system('clear' if sys.platform != 'win32' else 'cls')
            self.display.print_header("PENGATURAN")
            self.display.print_config_menu(self.num_threads, self.id_length)
            
            choice = input(f"{Fore.CYAN}Pilih [1-3]: {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self._change_threads()
            elif choice == '2':
                self._change_id_length()
            elif choice == '3':
                break
            else:
                self.display.print_error("Pilihan tidak valid!")
                time.sleep(1)
    
    def _change_threads(self):
        """Ubah jumlah thread"""
        print(f"\n{Fore.CYAN}Jumlah thread saat ini: {Fore.YELLOW}{self.num_threads}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Rekomendasi: 2-8 thread (sesuaikan dengan CPU cores){Style.RESET_ALL}\n")
        
        try:
            threads = int(input(f"{Fore.YELLOW}Masukkan jumlah thread (2-16): {Style.RESET_ALL}"))
            
            if threads < 2 or threads > 16:
                self.display.print_error("Jumlah thread harus antara 2-16!")
            else:
                self.num_threads = threads
                self.display.print_success(f"Jumlah thread diubah menjadi {threads}")
                time.sleep(1)
        
        except ValueError:
            self.display.print_error("Input tidak valid!")
            time.sleep(1)
    
    def _change_id_length(self):
        """Ubah panjang ID"""
        print(f"\n{Fore.CYAN}Panjang ID saat ini: {Fore.YELLOW}{self.id_length} digit{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Rekomendasi: 9-15 digit (default 11 digit){Style.RESET_ALL}\n")
        
        try:
            length = int(input(f"{Fore.YELLOW}Masukkan panjang ID (5-20): {Style.RESET_ALL}"))
            
            if length < 5 or length > 20:
                self.display.print_error("Panjang ID harus antara 5-20!")
            else:
                self.id_length = length
                self.display.print_success(f"Panjang ID diubah menjadi {length} digit")
                time.sleep(1)
        
        except ValueError:
            self.display.print_error("Input tidak valid!")
            time.sleep(1)
    
    def show_pattern_info(self):
        """Tampilkan informasi pola rare"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
        self.display.print_header("INFORMASI POLA RARE")
        self.display.print_pattern_info()
        
        print(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...{Style.RESET_ALL}")
        input()
    
    def read_results(self):
        """Baca file hasil"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
        self.display.print_header("BACA HASIL")
        
        output_dir = self.config.get('output_dir', './output')
        
        try:
            # Check file existence
            txt_file = os.path.join(output_dir, 'rare_ids.txt')
            json_file = os.path.join(output_dir, 'rare_ids.json')
            
            if not os.path.exists(txt_file) and not os.path.exists(json_file):
                self.display.print_warning("Belum ada hasil yang disimpan!")
                time.sleep(2)
                return
            
            print(f"\n{Fore.YELLOW}[1]{Style.RESET_ALL} Baca file TXT")
            print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Baca file JSON")
            print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Kembali\n")
            
            choice = input(f"{Fore.CYAN}Pilih [1-3]: {Style.RESET_ALL}").strip()
            
            if choice == '1' and os.path.exists(txt_file):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    print(f"\n{Fore.CYAN}{f.read()}{Style.RESET_ALL}")
            elif choice == '2' and os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"\n{Fore.CYAN}{json.dumps(data, indent=2, ensure_ascii=False)}{Style.RESET_ALL}")
            elif choice == '3':
                return
            else:
                self.display.print_error("File tidak ditemukan!")
                time.sleep(1)
            
            print(f"\n{Fore.YELLOW}Tekan Enter untuk kembali...{Style.RESET_ALL}")
            input()
        
        except Exception as e:
            self.display.print_error(f"Error membaca file: {str(e)}")
            self.storage.add_error(str(e), "file_read_error")
            time.sleep(2)
    
    def exit_app(self):
        """Exit aplikasi"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
        
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}{'TERIMA KASIH TELAH MENGGUNAKAN FF ID GENERATOR'.center(80)}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        # Show final statistics
        rare_ids = self.storage.get_rare_ids()
        if rare_ids:
            print(f"{Fore.GREEN}Total ID Rare Ditemukan: {len(rare_ids)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Hasil disimpan di folder 'output/'{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}\n")
        sys.exit(0)


def main():
    """Main entry point"""
    try:
        app = FFIDGeneratorApp()
        app.show_main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program dihentikan oleh user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Fatal Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
