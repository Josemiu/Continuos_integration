import math

class MembershipManager:
    """
    Gestión de costos de planes de membresía y funciones adicionales.
    Implementa la lógica de descuentos grupales, recargos y validaciones.
    """
    
    PLAN_COSTS = {
        "basic": 50,
        "premium": 100
    }
    
    FEATURE_COSTS = {
        "personal_training": 35,
        "specialized_training": 50
    }
    
    # specialized_training requiere recargo del 15% (Requisito 6)
    SURCHARGE_FEATURE = "specialized_training"
    SURCHARGE_RATE = 0.15 
    GROUP_DISCOUNT_RATE = 0.10
    GROUP_DISCOUNT_THRESHOLD = 3
    MAX_MEMBERS = 5
    FIXED_GROUP_DISCOUNT = 20.00

    def calculate_cost(self, plan: str, features: list, num_members: int, apply_group_discount: bool) -> int:
        """
        Calcula el costo total de la membresía.

        Args:
            plan (str): El tipo de plan de membresía.
            features (list): Lista de características adicionales.
            num_members (int): Número de miembros.
            apply_group_discount (bool): Si se debe aplicar el descuento grupal (10%).

        Returns:
            int: Costo total redondeado al entero más cercano, o -1 si es inválido.
        """

        # 1. Validación de Entrada (Requisito 9: Devuelve -1 si la entrada no es válida)
        if num_members <= 0 or num_members > self.MAX_MEMBERS:
            print("MENSAJE DE ERROR: Número de miembros inválido.")
            return -1
        
        if plan not in self.PLAN_COSTS:
            print(f"MENSAJE DE ERROR: Plan de membresía '{plan}' no válido.")
            return -1

        for feature in features:
            if feature not in self.FEATURE_COSTS:
                print(f"MENSAJE DE ERROR: Característica adicional '{feature}' no disponible.")
                return -1

        # Si todo es válido, calculamos el costo
        
        # 2. Cálculo del Costo Base por Miembro
        base_cost_per_member = self.PLAN_COSTS[plan]
        features_cost_per_member = sum(self.FEATURE_COSTS[f] for f in features)
        
        total_cost = (base_cost_per_member + features_cost_per_member) * num_members

        # 3. Aplicar Recargo (Surcharge) (Requisito 6) - Se aplica primero.
        if self.SURCHARGE_FEATURE in features:
            surcharge_amount = total_cost * self.SURCHARGE_RATE
            total_cost += surcharge_amount
            print(f"NOTIFICACIÓN: Se aplicó un recargo del {self.SURCHARGE_RATE * 100}% por '{self.SURCHARGE_FEATURE}'. Recargo: ${surcharge_amount:.2f}")

        # 4. Aplicar Descuento Grupal (Group Discount 10%) (Requisito 5)
        if apply_group_discount:
            discount_amount = total_cost * self.GROUP_DISCOUNT_RATE
            total_cost -= discount_amount
            print(f"NOTIFICACIÓN: Se aplicó un {self.GROUP_DISCOUNT_RATE * 100}% de descuento grupal. Ahorro: ${discount_amount:.2f}")

        # 5. Aplicar Descuento Fijo Adicional de $20.00
        # Se aplica solo para 2-3 miembros (con o sin descuento grupal)
        if num_members >= 2 and num_members <= 3:
            fixed_discount = self.FIXED_GROUP_DISCOUNT
            total_cost -= fixed_discount
            if apply_group_discount:
                print(f"NOTIFICACIÓN: Se aplicó un descuento fijo adicional de ${fixed_discount:.2f}.")
            else:
                print(f"NOTIFICACIÓN: Se aplicó un descuento fijo adicional de ${fixed_discount:.2f} por ser membresía de 2-3 miembros.")
            
        # 6. Salida Final y Redondeo
        return int(total_cost + 0.5)
