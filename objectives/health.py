import pygame

def draw_health_bar(screen, x, y, current_hp, max_hp):
    """
    Hàm vẽ thanh máu.
    :param screen: Màn hình game để vẽ lên
    :param x: Tọa độ ngang
    :param y: Tọa độ dọc
    :param current_hp: Máu hiện tại
    :param max_hp: Máu tối đa
    """
    # 1. Xử lý số liệu (tránh lỗi chia cho 0 hoặc máu âm)
    if current_hp < 0:
        current_hp = 0
    if max_hp <= 0: # Tránh lỗi chia cho 0
        ratio = 0
    else:
        ratio = current_hp / max_hp

    # 2. Cấu hình kích thước thanh máu
    bar_width = 200  # Chiều dài thanh máu
    bar_height = 20  # Chiều cao thanh máu
    
    # 3. Vẽ nền màu đỏ (phần máu đã mất)
    # Rect(x, y, width, height)
    pygame.draw.rect(screen, (200, 0, 0), (x, y, bar_width, bar_height))

    # 4. Vẽ phần màu xanh (máu còn lại)
    # Chiều dài màu xanh = Tổng chiều dài * tỷ lệ máu
    green_width = int(bar_width * ratio)
    if green_width > 0:
        pygame.draw.rect(screen, (0, 255, 0), (x, y, green_width, bar_height))

    # 5. Vẽ viền trắng bên ngoài cho đẹp
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)


def draw_lives(screen, x, y, lives, font):
    """
    Hàm vẽ số mạng sống (Lives).
    """
    # Tạo hình ảnh từ chữ
    text_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
    
    # Vẽ lên màn hình
    screen.blit(text_surface, (x, y))