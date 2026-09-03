"""
Module untuk menampilkan output di terminal dengan warna
"""

from colorama import Fore, Back, Style, init
import sys

# Inisialisasi colorama
init(autoreset=True)

class Display:
    """Kelas untuk menangani tampilan terminal"""
    
    @staticmethod
    def clear_screen():
        """Bersihkan layar terminal"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
    
    @staticmethod
    def print_header(title):
        """Tampilkan header dengan warna"""
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}{title.center(80)}")
        print(f"{Fore.CYAN}{'=' * 80}\n{Style.RESET_ALL}")
    
    @staticmethod
    def print_success(message):
        """Tampilkan pesan sukses"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(message):
        """Tampilkan pesan error"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_warning(message):
        """Tampilkan pesan warning"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(message):
        """Tampilkan pesan info"""
        print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_status_bar(current_id, total_generated, rare_count, speed, status="Running"):
        """
        Tampilkan status bar real-time
        
        Args:
            current_id: ID yang sedang diproses
            total_generated: Total ID yang sudah dihasilkan
            rare_count: Jumlah ID rare yang ditemukan
            speed: Kecepatan generator (ID/detik)
            status: Status generator
        """
        status_color = Fore.GREEN if status == "Running" else Fore.YELLOW
        
        print(f"\r{Fore.CYAN}[ID: {current_id}] " +
              f"{Fore.WHITE}| Generated: {total_generated} " +
              f"{Fore.MAGENTA}| Rare: {rare_count} " +
              f"{Fore.GREEN}| Speed: {speed:.0f} ID/s " +
              f"{status_color}| {status}{Style.RESET_ALL}", end='', flush=True)
    
    @staticmethod
    def print_menu():
        """Tampilkan menu utama"""
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}{'FREE FIRE ID GENERATOR - MAIN MENU'.center(80)}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        menu_items = [
            ("1", "Mulai Generator (Mode Normal)"),
            ("2", "Mulai Generator (Mode Custom Pattern)"),
            ("3", "Pengaturan Thread & ID Length"),
            ("4", "Lihat Info Pola Rare"),
            ("5", "Baca File Hasil"),
            ("6", "Exit")
        ]
        
        for key, description in menu_items:
            print(f"{Fore.YELLOW}[{key}]{Style.RESET_ALL} {description}")
        
        print()
    
    @staticmethod
    def print_pattern_info():
        """Tampilkan informasi pola rare"""
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}{'POLA RARE ID'.center(80)}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        patterns = [
            ("Kembar", "Angka kembar berturut-turut", "111, 222, 333", "Sangat Rare"),
            ("Berulang", "Pola ABA (digit pertama = digit ketiga)", "121, 131, 242", "Rare"),
            ("Urutan", "Urutan angka naik/turun", "123, 456, 789", "Sangat Rare"),
            ("Palindrome", "ID yang sama jika dibaca terbalik (min 5 digit)", "12321, 54345", "Extremely Rare"),
            ("Kombinasi Pendek", "Kombinasi unik pendek", "111222, 123321", "Very Rare")
        ]
        
        for name, desc, example, rarity in patterns:
            print(f"{Fore.GREEN}{name}:")
            print(f"  {Fore.WHITE}Deskripsi: {desc}")
            print(f"  {Fore.YELLOW}Contoh: {example}")
            print(f"  {Fore.MAGENTA}Kelangkaan: {rarity}\n")
    
    @staticmethod
    def print_statistics(total_generated, rare_count, duration, thread_count, avg_speed):
        """
        Tampilkan statistik akhir
        
        Args:
            total_generated: Total ID yang dihasilkan
            rare_count: Total ID rare yang ditemukan
            duration: Durasi runtime (detik)
            thread_count: Jumlah thread yang digunakan
            avg_speed: Rata-rata kecepatan ID/detik
        """
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}{'STATISTIK GENERATOR'.center(80)}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Total ID Dihasilkan: {Fore.YELLOW}{total_generated}")
        print(f"{Fore.WHITE}Total ID Rare: {Fore.MAGENTA}{rare_count}")
        print(f"{Fore.WHITE}Persentase Rare: {Fore.GREEN}{(rare_count/total_generated*100):.2f}%" if total_generated > 0 else f"{Fore.RED}0%")
        print(f"{Fore.WHITE}Durasi: {Fore.CYAN}{duration:.2f} detik")
        print(f"{Fore.WHITE}Thread Aktif: {Fore.BLUE}{thread_count}")
        print(f"{Fore.WHITE}Kecepatan Rata-rata: {Fore.YELLOW}{avg_speed:.0f} ID/s\n")
    
    @staticmethod
    def print_config_menu(current_threads, current_length):
        """Tampilkan menu konfigurasi"""
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}{'PENGATURAN GENERATOR'.center(80)}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Konfigurasi Saat Ini:")
        print(f"  {Fore.YELLOW}Thread: {Fore.GREEN}{current_threads}")
        print(f"  {Fore.YELLOW}Panjang ID: {Fore.GREEN}{current_length} digit\n")
        
        print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Ubah Jumlah Thread")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Ubah Panjang ID")
        print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Kembali ke Menu Utama\n")
    
    @staticmethod
    def print_loading_animation():
        """Tampilkan animasi loading"""
        animations = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        for anim in animations:
            print(f"\r{Fore.CYAN}{anim} Loading...{Style.RESET_ALL}", end='', flush=True)
            import time
            time.sleep(0.1)
        print()

import os
