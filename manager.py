# fse/core/manager.py
import asyncio
import logging
from typing import List

logger = logging.getLogger("FSE.Manager")

class FSEModuleManager:
    """መርህ #6: የቦቱን የተለያዩ ክፍሎች (Modules) በማስተዳደር ስራውን የሚያቀናጅ ክፍል ነው።"""
    def __init__(self):
        self.services: List = []
        self.running = False

    def register_service(self, service):
        """አዲስ አገልግሎት (እንደ ቴሌግራም ወይም ኤክስቼንጅ ኮኔክሽን) ለመመዝገቢያ።"""
        self.services.append(service)
        logger.info(f"Service registered: {service.__class__.__name__}")

    async def start_all(self):
        """መርህ #10: ሁሉንም አገልግሎቶች በአንድ ጊዜ ማስጀመሪያ።"""
        self.running = True
        logger.info("System Manager: Starting all services...")
        tasks = [service.run() for service in self.services]
        await asyncio.gather(*tasks)

    def shutdown(self):
        """መርህ #10: ሲስተሙን በንጽህና ማቆሚያ።"""
        self.running = False
        for service in self.services:
            if hasattr(service, 'stop'):
                service.stop()
        logger.info("System Manager: All services stopped.")
